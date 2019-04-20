#!/usr/bin/python3

''' Query and training methods for SRILM models'''

import json
import srilm
import math
import pandas as pd
import numpy as np
import lmz.utils

class srilm_model():

	def __init__(self, modelId, mode):

		self.metadata = lmz.utils.readJSONfromFile(os.path.join('metadata',modelId+'.json'))

		if mode == 'train':
			self.model = None 
			
			# !!! check the new model Id to make sure it doesn't exist yet if we are training a new one

			raise NotImplementedError
			# self.train()
		elif mode == 'retrain':
			# okay if the model already exist, 
			raise NotImplementedError

			# self.train()
		
		elif mode == 'query':
			self.model = self.load(modelId)

	def load(self, modelId):		
		path = os.path.join('data',modelId)
		return(srilm.LM(path))


	def getSurprisal(self, input, base):		
		
		#!!! use self.metadata to query different model types, e.g. no eos or sos
		all_utterances = []
		for input_row in input.to_dict('values'):

			utterance = np.array(['<s>']+ input_row['utterance'].strip().split(' ') + ['</s>'])

			word_probs = []            
			for i in range(1,len(utterance)):
				context = utterance[0:i][::-1]
			prob = self.lm.logprob_strings(utterance[i], context)
			word_probs.append({'word_index':i-1, 'word':utterance[i], 'log_prob':math.log(prob, base)})
			by_word_probs = pd.DataFrame(word_probs)
			by_word_probs['id'] = input_row['id']
			all_utterances.append(by_word_probs)

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