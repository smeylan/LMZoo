import pandas
import url

class LM_Zoo():
	
	def __init__(self, remote_url):
		raise NotImplementedError

		if not remote_url:
			print('Running LMZoo locally. Starting workers...')
			self.mode = 'local'				
			import queue # load only if we are running clients locally			
			self.LM_Queue = queue.LM_Queue()

		else:
			self.mode = 'remote'
			print('Directing requests to remote LMZoo server...')
			raise NotImplementedError

			print('Checking for heartbeat...')
			# check for a heartbeat with url

	
	def query(self, input, models, measures): 

		if self.mode == 'remote':			
			raise NotImplementedError
			# make a request to a server
			# parse a Python object

		elif self.mode == 'local': 
			result = self.LM_Queue.query(input, models, measures)
			return(result)