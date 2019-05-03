''' Generic celery worker that uses the modelId to load the correct model from lmz_api'''
''' note that the worker is associated with the queue from the command line invocation that launches this worker'''
''' eg "celery --app=lmz model_worker -Q "+modelId+" -c 1" '''

from celery import Celery
from celery.utils.log import get_task_logger
from celery.signals import worker_init, worker_process_init
from celery.concurrency import asynpool
from celery import signals
from celery.bin import Option
import json
import os

def readJSONfromFile(filename):
	with open(filename, 'r') as f:
	    datastore = json.load(f)
	return(datastore)


logger = get_task_logger(__name__)
app = Celery('tasks', backend='redis://localhost/0', broker='amqp://localhost')
app.conf.task_serializer   = 'json'
app.conf.result_serializer = 'json'

lm = None

def add_preload_options(parser):
    parser.add_argument(
        '-m', '--modelId', default=None,
        help='modelId to start for this queue')

app.user_options['preload'].add(add_preload_options)


@signals.user_preload_options.connect
def on_preload_parsed(options, **kwargs):
	# Stash modelId in the global vars b/c we can't pass options to worker init
    global modelId 
    modelId = options['modelId']    


@worker_process_init.connect()
def on_worker_init(**_): 	
	# make sure that the worker loads the correct specific model, consistent with this queue

	global modelId
	print('Worker received modelId:')
	print(modelId)
	
	metadata = readJSONfromFile(os.path.join('metadata',modelId+'.json'))
	
	# forgive me. better ideas welcome, but there are some constraints in the Celery workers
	exec_string = 'import lmz.api.'+metadata['type']+'_interface'
	exec(exec_string) # loads a model object, e.g. of class srilm

	global lm	
	# initialize a model in query mode
	lm = eval('lmz.api.'+metadata['type']+'_interface.'+metadata['type']+'_model(modelId,"query")')

@app.task
def query(input_dict_list, measures):
	print('Query called in worker')	
	global lm	
	result = lm.query_model(input_dict_list, measures)
	# because a specific model is loaded above, this will run the model-specific query code
	return(result)