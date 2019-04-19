# LMZoo: All The Language Models, All The Time
Language Model Zoo (LMZoo for brevity, or LMZ for... even more brevity) is a tool that makes it easy to retrieve probabilities from conditional language models. The main objective is to minimize the time required to retrieve word surprisal estimates for a broad range of models, i.e, allowing a researcher to retrieve probabilities of linguistic events using a  

`utt_measures = lmz.query(utterances, models='*', measures='*')`


It does this by 1) providing a standard Python API for a broad range of conditional langauge models 2) enforcing a metadata standard that makes data source and tokenziation explicit 3) providing infrastructure that abstracts away environment configuration from the end user, and allows for models with many different enviromental requirements (e.g., different Python or Tensorflow versions) to run concurrently. New models can be added to LMZ if they implement the appropriate methods and are documented with the model specification

LMZ is factored into 6 components

- *LMZ - Client* allows a user to send requests to a remote server
- *LMZ - Serve* handles these requests and adds them to a Celery task queue
- *LMZ - Self-Serve* allows a user to queue work in a local Celery queue
- *LMZ - Queue* spawn workers with appropriate environments to run different model architectures
- *LMZ - API* provides a layer that implements a set of standard language model tasks across a set of binding libraries for querying
- *LMZ - Train* provides a framework to train families of models using the metadata specification 

These components are described in greater detail below.

# LMZoo Client

- Pandas and R libraries
- Examples: `utt_surp = lmz.query(utterances, models='*', measures=['surprisal'])`, `utt_entropy = lmz.query(utterances, models='*', measures=['entropy'])`
- Sends GET request to LMZ - Serve (either on the local network or over the web)		 
- Also supplies a set of canned datasets, e.g., `childes_surp = lmz.query('childes_utterances', models='*', measures='*')`		


# LMZoo Serve
	
- Flask app that receives requests from the client to return one or more measures from one or more models, places tasks on the appropriate Celery queue


# LMZoo Self-Serve

- Python library run locally that places tasks on the appropriate Celery queues


# LMZoo Queue 

- Celery-based task queue, + methods to change it
- Starts workers as necessary, each with their own enviroments (following https://stackoverflow.com/questions/35700093/celery-django-daemon-multiple-virtual-environment)
- Specifies logic for cacheing results. For example, if a dataset is specified, the queue checks for a cached version of that dataset (rather than add a job to the queue)
- Celery task queue allows us to do scheduled tasks, like make the model cache results as models and datasets are added (if a training specification is provided to the model)


# LMZoo API

- Implements a set of methods for all models (compute permitting):
	
	`getSurprisal(utterances, base)` returns a suprisal estimate for every token
	`getPerplexity(utterances, base)` returns a float 
	`getEntropy(words, contexts, base)`  returns a vector of floats
	`getAvgInformationContent(words, base)` returns a vector of floats


- The API implements each of the above using existing binding libraries
	- pysrilm
	- SM wrapper for the Earley Parser
	- SM + SN wrapper for BLLIP
	- SM wrapper for BigLM
	- SM Google Books library
	


# LMZoo Train 

- Functions to train models with a metadata specification
- That model metadata is used in training and then also queryable from the client


# Metadata Specification

Queryable set of model parameters.

- `modelId`
- `dataSource`: reference to a local text file name
- `dataSourceHash`
- `tokenizationScheme`: name of tokenizer used
- `punctuationScheme`: include or exclude
- `sos`: include or exclude
- `eos`: include or exclude
- `implements`: list of methods implemented by this model
- `modelParameters`
	
	

# Supported models (by priority)
- SRILM / ARPA count files
- BigLM -- prioritize this because this is a good test of TensorFlow workers
- Gulordava LSTM
- KenLM
- Earley parser
- Google books (SM ngrawk library)	

# Model datasets (by priority)
- British National Corpus
- Penn TreeBank 
- CHILDES
- Switchboard
- Wikipedia
- Billion-Word Benchmark
- Reddit web text

# Runway
- [ ] Test whether the celery queue system works
- [ ] how to report progress from Celery before returning the final data
- [ ] How to deploy this as an appliance: get a local version running in Griffiths lab, etc.
- [ ] Relatedly, figure out how to hangle dependencies like SRILM (C++)  --  docker?