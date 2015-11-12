import logging, re
from itertools import chain
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, utils

from pprint import pprint

stoplist = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', '&', ':']

pattern = re.compile("[^\w\']+")

from pymongo import MongoClient
client = MongoClient()

db = client.jobstreet

collections = db.collection_names(include_system_collections=False)
iteration = [chain.from_iterable([pattern.sub(' ', entry["jd"].lower()).split() for entry in db[collection].find()]) for collection in collections]
dictionary = corpora.Dictionary()
iterable_count = 0
for iterable in iteration:
	collection_list = []
	count = 0
	for word in iterable:
		lem = utils.lemmatize(word)
		if len(lem)>0:
			count += 1
			processed_lem = lem[0].split('/')[0]
			collection_list.append(processed_lem)
			print collections[iterable_count] + ': ' + str(count)
	dictionary.add_documents([collection_list])
	iterable_count += 1
# dictionary = corpora.Dictionary([[utils.lemmatize(i)[0].split('/')[0] for i in chain.from_iterable([pattern.sub(' ', entry["jd"].lower()).split() for entry in db[collection].find()]) if len(utils.lemmatize(i))>0 ] for collection in collections[:1]])
stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
dictionary.filter_tokens(stop_ids+once_ids)
dictionary.compactify()
dictionary.save('./stores/jobs.dict')

dictionary2 = corpora.Dictionary([[utils.lemmatize(i)[0].split('/')[0] for i in chain.from_iterable([pattern.sub(' ', entry["title"].lower()).split() for entry in db[collection].find()]) if len(utils.lemmatize(i))>0 ] for collection in collections])
stop_ids2 = [dictionary2.token2id[stopword] for stopword in stoplist if stopword in dictionary2.token2id]
once_ids2 = [tokenid for tokenid, docfreq in dictionary2.dfs.iteritems() if docfreq == 1]
dictionary2.filter_tokens(stop_ids2+once_ids2)
dictionary2.compactify()
dictionary2.save('./stores/jobs_title.dict')

class MyCorpus(object):
	def __init__(self, collections, dictionary, attribute):
		self.collections = collections
		self.attribute = attribute
		self.dictionary = dictionary
	def __iter__(self):
		for collection in self.collections:
			yield self.dictionary.doc2bow([i for i in chain.from_iterable([entry[self.attribute].lower().split() for entry in db[collection].find()])])

corpus = MyCorpus(collections, dictionary, 'jd')
corpora.MmCorpus.serialize('./stores/corpus.mm', corpus)

corpus2 = MyCorpus(collections, dictionary2, 'title')
corpora.MmCorpus.serialize('./stores/corpus_title.mm', corpus2)