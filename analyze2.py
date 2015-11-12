from gensim import corpora, similarities, models
from pymongo import MongoClient
from pprint import pprint
from nltk.stem.wordnet import WordNetLemmatizer
import ast, sys, difflib, csv, re, signal, itertools
sys.settrace
lem = WordNetLemmatizer()

# def sig_handler(signum, frame):
# 	print 'segfault'
# signal.signal(signal.SIGSEGV, sig_handler)

string_out = ''

def extract(dict_in):
	if isinstance(dict_in, list):
		for item in dict_in:
			extract(item)
	elif isinstance(dict_in, dict):
	    for key, value in dict_in.iteritems():
	        if isinstance(value, dict): # If value itself is dictionary
	            extract(value)
	        elif isinstance(value, str) and value != 'text':
	            # Write to string_out
				global string_out
				string_out += ' ' +  value
	            # print string_out
	        elif isinstance(value, list):
	        	for item in value:
	        		extract(value)

def lemming(key):
	lemmed = lem.lemmatize(key)
	if lemmed == key:
		lemmed = lem.lemmatize(key, pos='v')
	return lemmed.lower()

terms = []
collections = []
with open('./careers.csv', 'Urb') as careersfile:
	reader = csv.reader(careersfile, delimiter=',', quotechar='"')
	reader.next()
	for row in reader:
		term = ast.literal_eval(row[3])
		term.append((row[2].lower(), 1.0))
		terms.append({'career': row[2], 'terms': term})
		collections.append(row[2])

def cleanUp(title):
	pattern = re.compile("[^\w\']+")
	return [lemming(key) for key in pattern.sub(' ', title).split()]

def keywordMatch(title):
	string_out = ''
	title = title.replace('\n','')
	try:
		dict_in = ast.literal_eval(title)
		extract(title)
	except:
		string_out = title
	title = cleanUp(string_out)
	string_out = ''
	return_list = [{'career':career, 'relevance':0} for career in collections]
	for token in title:
		match = [{'career': term_list['career'], 'relevance': sum([v for c,v in term_list['terms'] if difflib.SequenceMatcher(lambda x: 0, c, token).ratio()>0.9])} for term_list in terms]
		for i in xrange(len(match)):
			return_list[i]['relevance'] += match[i]['relevance']
	return sorted(return_list, key=lambda item:-item['relevance'])

def highestMatch(title):
	title = cleanUp(title)
	return sorted([{'career': cType, 'relevance': difflib.SequenceMatcher(lambda x: x in [' ', '&', '\''], title, cType).ratio()} for cType in collections], key=lambda item:-item['relevance'])


arg = ''
if len(sys.argv)>1:
	arg = sys.argv[1]

# client = MongoClient()
# db = client.jobstreet
# collections = db.collection_names(include_system_collections=False)

dictionary = corpora.Dictionary.load('./stores/jobs.dict')
dictionary2 = corpora.Dictionary.load('./stores/jobs_title.dict')
dictionary3 = dictionary.merge_with(dictionary2)
corpus = corpora.MmCorpus('./stores/corpus.mm')
corpus2 = corpora.MmCorpus('./stores/corpus_title.mm')
corpus3 = itertools.chain(corpus, dictionary3[corpus2])

if arg == 'new':
	tfidf = models.TfidfModel(corpus3)
	tfidf.save('./stores/jobs.tfidf')
else:
	tfidf = models.TfidfModel.load('./stores/jobs.tfidf')

corpus_tfidf = tfidf[corpus3]

if arg == 'new':
	lsi = models.LsiModel(corpus_tfidf, id2word=dictionary3, num_topics=400)
	lsi.save('./stores/jobs.lsi')
else:
	lsi = models.LsiModel.load('./stores/jobs.lsi')

corpus_lsi = lsi[corpus_tfidf]

if arg=='new':
	index_lsi = similarities.Similarity('/tmp/shards/', corpus_lsi, num_features=400)
	index_lsi.save('./stores/jobs_lsi.index')
else:
	index_lsi = similarities.Similarity.load('./stores/jobs_lsi.index')

if arg=='new':
	index_tfidf = similarities.Similarity('/tmp/shards/', corpus_tfidf, num_features=26663)
	index_tfidf.save('./stores/jobs_tfidf.index')
else:
	index_tfidf = similarities.Similarity.load('./stores/jobs_tfidf.index')

def jd_tfidf(doc):
	vec_bow = dictionary3.doc2bow(cleanUp(doc))
	vec_tfidf = tfidf[vec_bow]

	sims_tfidf = index_tfidf[vec_tfidf]
	sims_tfidf_list = []
	for (id, score) in list(enumerate(sims_tfidf)):
		sims_tfidf_list.append({'career': collections[id], 'relevance': score})
	return sorted(sims_tfidf_list, key=lambda x:-x['relevance'])

def jd_lsi(doc):
	string_out = ''
	doc = doc.replace('\n','')
	try:
		dict_in = ast.literal_eval(doc)
		extract(dict_in)
	except:
		string_out = doc

	vec_bow = dictionary3.doc2bow(cleanUp(string_out))
	string_out = ''
	vec_lsi = lsi[vec_bow]
	sims_lsi = index_lsi[vec_lsi]
	sims_lsi_list = []
	for (id, score) in list(enumerate(sims_lsi)):
		sims_lsi_list.append({'career': collections[id], 'relevance': score})
	return sorted(sims_lsi_list, key=lambda x:-x['relevance'])


# Titles

if arg=='new':
	tfidf2 = models.TfidfModel(corpus3)
	tfidf2.save('./stores/jobs_title.tfidf')
else:
	tfidf2 = models.TfidfModel.load('./stores/jobs_title.tfidf')

corpus_tfidf2 = tfidf2[corpus3]

if arg=='new':
	lsi2 = models.LsiModel(corpus_tfidf2, id2word=dictionary3, num_topics=400)
	lsi2.save('./stores/jobs_title.lsi')
else:
	lsi2 = models.LsiModel.load('./stores/jobs_title.lsi')

corpus_lsi2 = lsi2[corpus_tfidf2]


if arg=='new':
	index_tfidf2 = similarities.Similarity('/tmp/shards2/', corpus_tfidf2, num_features=4480)
	index_tfidf2.save('./stores/jobs_title_tfidf.index')
else:
	index_tfidf2 = similarities.Similarity.load('./stores/jobs_title_tfidf.index')

if arg=='new':
	index_lsi2 = similarities.Similarity('/tmp/shards2/', corpus_lsi2, num_features=400)
	index_lsi2.save('./stores/jobs_title_lsi.index')
else:
	index_lsi2 = similarities.Similarity.load('./stores/jobs_title_lsi.index')

def title_tfidf(doc2):
	vec_bow2 = dictionary3.doc2bow(cleanUp(doc2))
	vec_tfidf2 = tfidf2[vec_bow2]

	sims_tfidf2 = index_tfidf2[vec_tfidf2]
	sims_tfidf_list2 = []
	for (id, score) in list(enumerate(sims_tfidf2)):
		sims_tfidf_list2.append({'career': collections[id], 'relevance': score})
	return sorted(sims_tfidf_list2, key=lambda x:-x['relevance'])

def title_lsi(doc2):
	vec_bow2 = dictionary3.doc2bow(cleanUp(doc2))
	vec_lsi2 = lsi2[vec_bow2]

	sims_lsi2 = index_lsi2[vec_lsi2]
	sims_lsi_list2 = []
	for (id, score) in list(enumerate(sims_lsi2)):
		sims_lsi_list2.append({'career': collections[id], 'relevance': score})
	return sorted(sims_lsi_list2, key=lambda x:-x['relevance'])