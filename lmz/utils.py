#!/usr/bin/python3

''' Shared convenience functions '''

import json

def readJSONfromFile(filename):
	with open(filename, 'r') as f:
	    datastore = json.load(f)
	return(datastore)