''' Query and training methods for SRILM models'''

import json
from srilm import LM
import math
import pandas as pd
import numpy as np
import lmz.utils
import os
import time

class srilm_model():

	def __init__(self, modelId, mode):

		self.metadata = lmz.utils.readJSONfromFile(os.path.join('metadata',modelId+'.json'))

		if mode == 'train':
			self.model = None 
			
			# !!! check the new modelId to make sure it doesn't exist among the metadata collection

			raise NotImplementedError
			# self.train()
		elif mode == 'retrain':
			# okay if the model already exist, 
			raise NotImplementedError

			# self.train()
		
		elif mode == 'query':
			self.model = self.load(modelId)

	def load(self, modelId):		
		t1 = time.time()
		print('Loading model for '+modelId+'...')
		path = os.path.join('data',modelId+'.LM')
		loaded_model = LM(path, lower=True)
		print('Finished loading model '+modelId+' in '+str(round(time.time() - t1))+' seconds')
		return(loaded_model)

	def query_model(self, input_dict_list, measures, base=2):
		print('Query called in srilm_model')

		#!!! logic for calling multiple measures (*) on the same model goes here; checking against the metadata
		rdf = self.getSurprisal(input_dict_list, base)
		rlist = rdf.to_dict('records')
		# returns a dataframe
		return(rlist) # need to be a list for serialization

	def getSurprisal(self, input_dict_list, base, verbose=False):		
		
		#!!! use self.metadata to query different model types, e.g. no eos or sos
		all_utterances = []
		for input_row in input_dict_list:

			utterance = np.array(['<s>']+ [x.lower() for x in input_row['utterance'].strip().split(' ')] + ['</s>'])

			word_probs = []            
			for i in range(0,len(utterance)):				
				context = utterance[0:i][::-1]
				if len(context) > 2:
					context = context[0:2] #!!! soft code the max length of the context; pull this from the model metadata
			
				srilm_output = self.model.logprob_strings(utterance[i], context)
				if verbose:
					print('utterance: '+utterance[i])
					print('context: ')
					print(context)
					print(prob)
				if not np.isinf(srilm_output): 
					surprisal = -1. * math.log(10. ** srilm_output, base)
				else:					
					surprisal = None					
				word_probs.append({'word_index':i-1, 'word':utterance[i], 'log_prob':surprisal})
			
			by_word_probs = pd.DataFrame(word_probs)
			by_word_probs['id'] = input_row['id']
			all_utterances.append(by_word_probs)

		# returns a dataframe
		print('X Computed all surprisal estimates.')
		return(pd.concat(all_utterances))


	def getEntropy(self, input, base):
		# operation on self.getSurprisal
		raise NotImplementedError 

	def getPerplexity(self, input, base, normalize):

		surprisal = self.getSurprisal(input, base)
		
		# !!! sum of the surprisal estimates		
		ppl = np.sum(surprisal['log_prob'])
		if normalize:
			return(ppl / float(len(surprisal)))
		else:
			return(ppl)

	def generateText(self, input, base, normalize):

		# operation on self.getSurprisal()
		raise NotImplementedError


	def train(self, metadata):
		# model-specific training logic using information in the metadata object
		raise NotImplementedError #DTROTFO		