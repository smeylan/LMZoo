''' Queue and Celery worker management'''

import pandas as pd
from joblib import Parallel, delayed  
import os
import model_worker
import glob
import lmz.utils
import subprocess
from functools import reduce

def bash_command(cmd):
    subprocess.Popen(['/bin/bash', '-c', cmd])

def initCeleryQueueSingletonWorker(modelId):
	print('Starting celery worker for model '+modelId)	
	
	metadata = lmz.utils.readJSONfromFile(os.path.join('metadata',modelId+'.json'))
	print(metadata)
	venv_command = "source "+os.path.join('environments',metadata['env_name'],'bin','activate') # Can get the venv_command from the metadata specification
	command = ' && '.join([venv_command, "celery --app=model_worker  worker -Q ", modelId," -c 1 -m ", modelId ])

	#!!! generate a unique ID for each worker that can later be pkilled rather than searching by the modelId with pkill -f

	print('Starting worker with command:')
	print(command)
	bash_command(command)

def killCeleryQueueSingletonWorker(modelId):	
	print('Stopping celery worker for model '+modelId)
	command = "pkill -9 -f '"+modelId+"'"
	os.system(command)

def addModelIdToColNames(columnNames, modelId):
	'''rename columns except "id" with the format $modelId_$measure'''
	return([modelId+'-'+x if x != 'id' else 'id' for x in columnNames])


def getFromCeleryQueueSingletonWorker(input_dict_list, modelId, measures):

	print('Getting measures ['+str(', '.join(measures))+'] from '+modelId+' in Celery worker')

	# this starts a celery queue for this specific model
	initCeleryQueueSingletonWorker(modelId)

	# results from the Celery workers are a list of dictionaries; build them back into a DF
	model_result_list = model_worker.query.apply_async([input_dict_list, measures], queue=modelId).get()
	model_result_df = pd.DataFrame(model_result_list)
	
	# add the model name for the measures in the DF, appropriate for merging 
	model_result_df.columns = addModelIdToColNames(model_result_df.columns, modelId)

	# stop the spawned worker
	killCeleryQueueSingletonWorker(modelId)

	return(model_result_df)

def recursive_merge(dataframes, merge_columns):
	# given results from n > 0 models, merge the results for each token
	return(reduce(lambda  left,right: pd.merge(left,right,on=merge_columns,
                                            how='outer'), dataframes))

class LM_Queue():

	def __init__(self, num_cores=8, preload_models=[]):
		self.num_cores = num_cores
		if len(preload_models) == 0:
			print('No model preloading selected.')
		else:
			for modelId in preload_models:
				initCeleryQueueSingletonWorker(modelId)
				# note that the models are identified by the queue name

	def query(self, inputListOrString, modelIds, measures):
		print('Querying the model...')
		# input either in the format 
			# [['s1t1', 's1t2'],['s2t1','s2t2']]: set of utterances to compute surprisal estimates
			# string:  name of a dataset
		if modelIds == '*':
			# load the set of all models from the metadata folder
			metadata_specs = glob.glob('metadata/*.json')			
			modelIds = [os.path.basename(x).replace('.json','') for x in metadata_specs]

		if type(inputListOrString) is str:
			print('Retrieving cached results for dataset: '+input)
			raise NotImplementedError
			cachedResult = None #DTROTFO: loading a pre-run model, either to get back results for the dataset specified by the string or the set of utterances in inputDForString
			return(cachedResult)

		elif type(inputListOrString) is list:

			# change it to a dataframe
			inputDForString = pd.DataFrame({'utterance':inputListOrString})
			inputDForString['id'] = range(inputDForString.shape[0])
			# this is a df with id and utterance (a string) for each record
			
			# serialize before sending into parallel
			input_dict_list = inputDForString.to_dict('records')

			#  Parallel wrapper blocks until we get all results from the Celery workers inside the jobs
			# returns a list of dataframes, one per model 		
			celery_results = Parallel(n_jobs=self.num_cores)(
				delayed(getFromCeleryQueueSingletonWorker)(input_dict_list, modelId, measures)  for modelId in modelIds)
			print('Finished parallel stage, merging results...')

			
			print('Merging results...')
			merged_results = recursive_merge(celery_results, ['id'])
			print('Finished merging results...')
			return(merged_results)