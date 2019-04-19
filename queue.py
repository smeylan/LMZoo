import pandas as pd
from joblib import Parallel, delayed  
import os
import model_worker

def initCeleryQueueSingletonWorker(modelId):
	print('Starting celery worker for model '+modelId)	
	venv_command = '' # Can get the venv_command from the metadata specification
	command = ' '.join(venv_command, "celery --app=lmz model_worker -Q "+modelId+" -c 1")
	os.system(command)	

def killCeleryQueueSingletonWorker(modelId):	
	print('Stopping celery worker for model '+modelId)
	command = "pkill -9 -f '"+modelId+"'"
	os.system(command)


def getFromCeleryQueueSingletonWorker(input_df, modelId, measures):
	print('Getting'+str(' '.join(measures))+' from '+modelId+' in Celery worker')

	# this starts a celery queue for this specific model
	initCeleryQueueSingletonWorker(modelId)
	model_results = model_worker.query.apply([input_df, measures],queue=modelId) 
	killCeleryQueueSingletonWorker(modelId)

	return(model_results)

def recursive_merge(dataframes, merge_columns):
	# given results from n > 0 models, merge the results for each token
	raise NotImplementedError
	#DTROTFO

class LM_Queue():

	def __init__(self, num_cores=8):
		pass
		# DTROTFO: pre-load the models

	def query(self, input, models, measures):
		# input either in the format 
			# [['s1t1', 's1t2'],['s2t1','s2t2']]: set of utterances to compute surprisal estimates
			# string:  name of a dataset

		initCeleryQueueSingletonWorker(model)

		if type(input) is str:
			print('Retrieving cached results for dataset: '+input)
			raise NotImplemtedError
			cachedResult = None #DTROTFO
			return(cachedResult)
		
		# give a unique id to the utterances
		input_df = pd.DataFrame({'input'})
		input_df['id'] = input_df.shape[0]

		#  Parallel halts until we get all results from apply_sync in celery 		
		
		celery_results = Parallel(n_jobs=num_cores)(
			delayed(runModelInCeleryWorker)(input_df, model, measures)  for i in models) 		

		merged_results = recursive_merge(celery_results, 'id')
		return(merged_results)