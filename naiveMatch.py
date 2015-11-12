import csv, os, nltk, difflib, operator, pprint
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

stop = stopwords.words('english')
stop.extend('&')
lem = WordNetLemmatizer()

jobs = [];
careers = [];

with open('./public_Jobs.csv', 'Urb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	reader.next()
	for row in reader:
		jobs.append(row)

with open('./careers.csv', 'Urb') as careersfile:
	reader = csv.reader(careersfile, delimiter=',', quotechar='"')
	reader.next()
	for row in reader:
		careers.append(row)

def lemming(key):
	lemmed = lem.lemmatize(key)
	if lemmed == key:
		lemmed = lem.lemmatize(key, pos='v')
	return lemmed.lower()

careerTypes = []

for career in careers:
	careerTypes.append(lemming(career[2]))

def highestMatch(term):
	scores = []
	for cType in careerTypes:
		score = difflib.SequenceMatcher(lambda x: x in [' ', '&', '\''], term, cType).ratio()
		scores.append(score)
	maxIndex, maxValue = max(enumerate(scores), key=operator.itemgetter(1))
	return careerTypes[maxIndex], maxValue

def longestMatch(term):
	scores = []
	for cType in careerTypes:
		score = difflib.SequenceMatcher(lambda x: x in [' ', '&', '\''], term, cType).find_longest_match(0, len(term), 0, len(cType))
		scores.append(score.size)
	maxIndex, maxValue = max(enumerate(scores), key=operator.itemgetter(1))
	return careerTypes[maxIndex], maxValue

conversionCount = 0
jobCount = 0

suspectList = []

for job in jobs:
	jobCount += 1
	term = lemming(job[2])
	cType, matchValue = highestMatch(term)
	if matchValue>=0.5:
		if matchValue < 1:
			suspectList.append((cType, term, matchValue))
			# print '%(term)s -> %(cType)s = %(matchValue)s' % {"term": term, "cType": cType, "matchValue": matchValue}
		conversionCount += 1
	else:
		if term != 'null' and bool(term):
			cType2, matchValue2 = longestMatch(term)
			if matchValue2 >= 5:
				conversionCount = conversionCount
				# conversionCount += 1
				# print '%(term)s -> %(cType)s = %(matchValue)s' % {"term": term, "cType": cType2, "matchValue": matchValue2}

pprint.pprint(sorted(suspectList, key=lambda score:score[2], reverse=True))
print '%(c)s / %(j)s' % {"c": conversionCount, "j": jobCount}