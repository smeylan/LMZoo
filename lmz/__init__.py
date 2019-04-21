'''Manages a connection to a server or initiates a queue locally to process requests'''

import urllib
import lmz.lmz_queue
import lmz.api

class LM_Zoo():
	
	def __init__(self, remote_url=None):

		if not remote_url:
			print('Running LMZoo locally. Starting workers...')
			self.mode = 'local'				
			import queue # load only if we are running clients locally			
			self.LM_Queue = lmz_queue.LM_Queue()

		else:
			self.mode = 'remote'
			print('Directing requests to remote LMZoo server...')
			raise NotImplementedError			

			print('Checking for heartbeat...')
			# check for a heartbeat with urllib on the remote machine

	
	def query(self, inputListOrString, modelIds, measures): 
		# input is dataframe or string

		if self.mode == 'remote':			
			raise NotImplementedError
			# make a request to a server
			# parse a Python object

		elif self.mode == 'local': 
			result = self.LM_Queue.query(inputListOrString, modelIds, measures)
			return(result)