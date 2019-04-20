import srilm

class SRILM_Model():

	def __init__(self, modelId, mode, metadata=None):
		

		if mode == 'train':
			self.model = None 
			if metadata is None:
				Raise ValueError('Metadata must be specified if mode is train')


			# check the new model Id to make sure it doesn't exist yet

			# self.train()
		elif mode == 'retrain':
			# okay if the model already exist, 
			raise NotImplementedError

			# self.train()
		
		elif mode == 'query':
			self.model = self.load(modelId)

	def load(self, modelId):		
		path = None #!!! get the translation from modelId to path using the metadata specification
		return(srilm.LM(path))


	def getSurprisal(self, input, base):
		for utterance in input:
			for word in utterance:
				# self.model.logprob(i, context) -- see the other code I've written
				raise NotImplementedError


	def getEntropy(self, input, base):
		# operation on self.getSurprisal
		raise NotImplementedError 

	def getPerplexity(self, input, base, normalize):

		# operation on self.getSurprisal()
		raise NotImplementedError


	def generateText(self, input, base, normalize):

		# operation on self.getSurprisal()
		raise NotImplementedError


	def train(self, metadata):
		# model-specific training logic using information in the metadata object
		raise NotImplementedError #DTROTFO		