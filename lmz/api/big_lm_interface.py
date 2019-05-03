import os
import sys
sys.path.append('/home/stephan/python/lm_1b/lm_1b') #!!! this needs to be generalized
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' #suppress memory warnings from Tensorflow
import lm_1b_persistent #this is a special version of LM1B that keeps the model in memory 
import lmz.utils

class big_lm_model():

	def __init__(self, modelId, mode):

		self.metadata = lmz.utils.readJSONfromFile(os.path.join('metadata',modelId+'.json'))

		#pbtxt_path = 'data/graph-2016-09-10.pbtxt'
		#ckpt_path = 'data/ckpt-*'
		#vocab_path = 'data/vocab-2016-09-10.txt'

		self.model = lm_1b_persistent.LM1B_model(self.metadata) 


	def query_model(self, input_dict_list, measures, base=2):
		print('Query called in srilm_model')

		#!!! logic for calling multiple measures (*) on the same model goes here; checking against the metadata
		rdf = self.getSurprisal(input_dict_list, base)
		rlist = rdf.to_dict('records')
		# returns a dataframe
		return(rlist) # need to be a list for serialization


	def getSurprisal(self, input_dict_list, base, verbose=False):
		# input_dict_list is a list of dictionaries with utterance_id, utterances as lists, token_ids as lists (cast from a dataframe)
		# how much of this should go here rather than in the lm_1b_persistent code?

		test = self.model._EvalSentencesDicts(input_dict_list, base)
		# already a dataframe
		return(test)
