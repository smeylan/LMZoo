import argparse
import lmz_api
from celery import Celery
from celery.utils.log import get_task_logger
from celery.signals import worker_init, worker_process_init
from celery.concurrency import asynpool

# argparse lets us spawn the celery workers programatically for different models
# recall that they may have different environments

parser = argparse.ArgumentParser()
parser.add_argument("", help="Name of the model to initalize")
args = parser.parse_args()

logger = get_task_logger(__name__)
app = Celery(modelId, backend='redis://localhost/0', broker='amqp://localhost')
app.conf.task_serializer   = 'json'
app.conf.result_serializer = 'json'

@worker_process_init.connect()
def on_worker_init(**_, modelId): #check if this works
	eval('import lmz_api.'+modelId)
	lm = eval('lmz_api.'+modelId+'()')

@app.task
def query()
	result = lm.query(input_df, measures) # because a specific model is loaded above, this will run the model-specific query code
	return(result)