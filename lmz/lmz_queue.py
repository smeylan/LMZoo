#!/usr/bin/python3

''' Queue and Celery worker management'''

import pandas as pd
from joblib import Parallel, delayed  
import os
import model_worker
import glob

def initCeleryQueueSingletonWorker(modelId):
	print('Starting celery worker for model '+modelId)	
	venv_command = '' # Can get the venv_command from the metadata specification
	command = ' '.join([venv_command, "celery --app=tasks model_worker -Q "+modelId+" -m "+modelId+" -c 1"])
	print('Starting worker with command:')
	print(command)
	os.system(command)	

def killCeleryQueueSingletonWorker(modelId):	
	print('Stopping celery worker for model '+modelId)
	command = "pkill -9 -f '"+modelId+"'"
	os.system(command)

def addModelIdToColNames(columnNames, modelId):
	'''rename columns except "id" with the format $modelId_$measure'''
	return([modelId+'_'+x if x != 'id' else 'id' for x in columnNames])


def getFromCeleryQueueSingletonWorker(input_df, modelId, measures):
	print('Getting measures ['+str(', '.join(measures))+'] from '+modelId+' in Celery worker')

	# this starts a celery queue for this specific model
	initCeleryQueueSingletonWorker(modelId)
	model_results = model_worker.query.apply([input_df, measures],queue=modelId) 	
	model_results.columns = addModelIdToColNames(model_results.columns)#<---

	killCeleryQueueSingletonWorker(modelId)

	return(model_results)

def recursive_merge(dataframes, merge_columns):
	# given results from n > 0 models, merge the results for each token
	return(reduce(lambda  left,right: pd.merge(left,right,on=merge_columns,
                                            how='outer'), dataframes))

class LM_Queue():

	def __init__(self, num_cores=8, preload_models=[]):
		self.num_cores = 8
		if len(preload_models) == 0:
			print('No model preloading selected.')
		else:
			for modelId in preload_models:
				initCeleryQueueSingletonWorker(modelId)
				# note that the models are identified by the queue name

	def query(self, input, modelIds, measures):
		# input either in the format 
			# [['s1t1', 's1t2'],['s2t1','s2t2']]: set of utterances to compute surprisal estimates
			# string:  name of a dataset
		if modelIds == '*':
			# load the set of all models from the metadata folder
			metadata_specs = glob.glob('metadata/*.json')			
			modelIds = [os.path.basename(x).replace('.json','') for x in metadata_specs]

		for modelId in modelIds:
			initCeleryQueueSingletonWorker(modelId)

		if type(input) is str:
			print('Retrieving cached results for dataset: '+input)
			raise NotImplementedError
			cachedResult = None #DTROTFO: loading a pre-run model
			return(cachedResult)
		
		# give a unique id to the utterances
		input_df = pd.DataFrame({'input'})
		input_df['id'] = input_df.shape[0]

		#  Parallel wrapper blocks until we get all results all workers (synchronous) in celery
		celery_results = Parallel(n_jobs=self.num_cores)(
			delayed(getFromCeleryQueueSingletonWorker)(input_df, modelId, measures)  for modelId in modelIds) 		

		merged_results = recursive_merge(celery_results, ['id'])
		return(merged_results.to_dict('values'))