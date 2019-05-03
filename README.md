# LMZoo: All The Language Models, All The Time
Language Model Zoo (LMZoo for brevity, or LMZ for... even more brevity) is a tool that makes it easy to retrieve probabilities from conditional language models. The main objective is to minimize the time required to retrieve word surprisal estimates for a broad range of models, i.e, allowing a researcher to retrieve probabilities of linguistic events using minimal code, for example: 

`utt_measures = lmz.query(utterances, models='*', measures='*')`


It does this by 1) providing a standard Python API for a broad range of conditional langauge models 2) enforcing a metadata standard that makes data source, eos and bos markers, and tokenziation explicit 3) providing infrastructure that abstracts away environment configuration from the end user, and allows for models with many different enviromental requirements (e.g., different Python or Tensorflow versions) to run concurrently. New models can be added to LMZ if they implement the appropriate methods (described below) and are documented with the model specification

As of May 2019, LMZoo can run models from SRILM and the Jozefowicz et al. (2016) "Big LM" model:

```
Finished merging results...
    big_lm-log_prob  token_id  utterance_id big_lm-word  bnc_knn_trigram-log_prob bnc_knn_trigram-word
0               NaN         0             0         <S>                       NaN                  <s>
1          2.804725         1             0         The                  3.292520                  the
2         18.952526         2             0       quick                 14.702216                quick
3         17.508516         3             0       brown                 13.449099                brown
4         10.830424         4             0         fox                 17.090309                  fox
5         11.011580         5             0      jumped                 12.366084               jumped
6          4.288494         6             0        over                  6.140744                 over
7          2.518478         7             0         the                  0.811477                  the
8         16.205176         8             0        lazy                 16.896229                 lazy
9          8.929297         9             0        dogs                 15.614229                 dogs
10         3.946162        10             0           .                 26.875089                    .
11         2.893546        11             0        </S>                  4.506063                 </s>
12              NaN         0             1         <S>                       NaN                  <s>
13         2.691840         1             1         The                  3.292520                  the
14        18.483486         2             1       horse                 11.268004                horse
15        11.462977         3             1       raced                 14.964711                raced
16         5.029307         4             1        past                  6.399983                 past
17         2.272531         5             1         the                  3.313860                  the
18         9.075620         6             1        barn                 14.462418                 barn
19        17.802300         7             1        fell                 16.015275                 fell
20         5.970849         8             1           .                 27.718202                    .
21         0.575794         9             1        </S>                  4.506063                 </s>

```

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

- Python module with maximal abstraction. This is the `lmz` module in `utt_measures = lmz.query(utterances, models='*', measures='*')`. Serve can call this


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
	- [x] pysrilm
	- [ ] SM wrapper for the Earley Parser
	- [ ] SM + SN wrapper for BLLIP
	- [x] SM wrapper for BigLM
	- [ ] SM Google Books library
	


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
- `sos`: empty string or sos marker
- `bos`: empty string or bos marker
- `implements`: list of methods implemented by this model
- `modelParameters`
	
	

# Supported models (by priority)
- [x] SRILM / ARPA count files
- [x] BigLM -- prioritize this because this is a good test of TensorFlow workers
- [ ] Gulordava LSTM
- [ ] KenLM
- [ ] Earley parser
- [ ] Google books (SM ngrawk library)	

# Model datasets (by priority)
- [ ] British National Corpus
- [ ] Penn TreeBank 
- [ ] CHILDES
- [ ] Switchboard
- [ ] Wikipedia
- [ ] Billion-Word Benchmark
- [ ] Reddit web text

*Note*: Availability of datasets * models should be described in a table, with some elements missing for copyright, compute, etc.

# Installation

- Install Redis if necessary, start a server
- Install AMPQ if necessary, and start
- Make a virtualenv with Python 3.5+ in the root and install requirements there
- For each model, make a virtualenv with the appropriate Python version and install the specific requirements file and all dependencies specified in the metadata
- Run the hello world:`client_example.py`


# Runway
- [x] Test whether the celery queue system works -- Yes as of 4/21
- [x] Confirm that Tensorflow works within a Celery worker
- [ ] implement other measures (esp. entropy)
- [ ] how to report progress from Celery before returning the final data? 
- [ ] How to deploy this as an appliance: get a local version running in Griffiths lab, etc.
- [ ] Relatedly, figure out how to hangle dependencies like SRILM (C++)  --  docker?