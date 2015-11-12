import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities

documents = ["Human machine interface for lab abc computer applications",
			"A survey of user opinion of computer system response time",
			"The EPS user interface management system",
			"System and human system engineering testing of EPS",
			"Relation of user perceived response time to error measurement",
			"The generation of random binary unordered trees",
			"The intersection graph of paths in trees",
			"Graph minors IV Widths of trees and well quasi ordering",
			"Graph minors A survey"]

stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
		for document in documents]

from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
	for token in text:
		frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1]
		for text in texts]

dictionary = corpora.Dictionary(texts)
dictionary.save('./deerwester.dict')

new_doc = "Human Computer Interaction"
new_vec = dictionary.doc2bow(new_doc.lower().split())
# print new_vec

corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('./deerwester.mm', corpus)
# print(corpus)

class MyCorpus(object):
	def __iter__(self):
		for line in open('mycorpus.txt'):
			yield dictionary.doc2bow(line.lower().split())

corpus_memmory_friendly = MyCorpus()
for vector in corpus_memmory_friendly:
	# print vector
	pass

texts2 = [[word for word in line.lower().split() if word not in stoplist] for line in open('mycorpus.txt')]
frequency2 = defaultdict(int)
for text in texts2:
	for token in text:
		frequency2[token] += 1

texts2 = [[token for token in text if frequency2[token]>1] for text in texts2]
print texts
print texts2
dictionary2 = corpora.Dictionary(texts2)
dictionary2.save('./deerwester2.dict')

dictionary2 = corpora.Dictionary.load('./deerwester2.dict')
print dictionary.token2id
print dictionary2.token2id

corpus3 = corpora.MmCorpus('./deerwester.mm')

tfidf = models.TfidfModel(corpus3)
doc_bow = [(0, 1), (1, 1)]
# print(tfidf[doc_bow])

corpus_tfidf = tfidf[corpus3]
for doc in corpus_tfidf:
	# print doc
	pass

lsi = models.LsiModel(corpus_tfidf, id2word=dictionary2, num_topics=2)
corpus_lsi = lsi[corpus_tfidf]
lsi.print_topics(2)

for doc in corpus_lsi:
	print doc

lsi.save('./model.lsi') 
lsi = models.LsiModel.load('./model.lsi')

doc = "Human computer interaction"
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow]

index = similarities.MatrixSimilarity(lsi[corpus3])
index.save('./deerwester.index')
index = similarities.MatrixSimilarity.load('./deerwester.index')

sims = index[vec_lsi]
sims = sorted(enumerate(sims), key=lambda item: -item[1])
for rank in sims:
	print rank
