#!/usr/bin/python3

'''client example. Load model and query utterances'''

import lmz

LMZ = lmz.LM_Zoo()

utterances = [
	'The quick brown fox jumped over the lazy dogs .',
	'The horse raced past the barn fell .'
]

result = LMZ.query(utterances, modelIds="*", measures="*")
print(result)