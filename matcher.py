import csv, os, requests, operator, ast, re, nltk, string
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

proxies = {
  "http": "213.85.92.10:80"
}
stop = stopwords.words('english')
stop.extend('&')
lem = WordNetLemmatizer()
twinword = 'https://www.twinword.com/api/v4/word/associations/'

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

def getAssoc(term):
	if term == 'Entrepreneurship':
			term = 'Entrepreneur'
	data = {'entry': term}
	semanticLink = 'http://semantic-link.com/related.php?word=' + term
	t = requests.post(twinword, data=data, proxies=proxies)
	try:
		associations = t.json()['associations_scored']
	except:
		print 'ERROR! ', term, t.text
		print requests.get('https://api.ipify.org?format=json', proxies=proxies).json()
		associations = {}
	s = requests.get(semanticLink)
	association2 = s.json()
	for key in associations:
		key = lemming(key)

	for assoc in association2:
		lemmed = lemming(assoc['v'])
		if lemmed not in associations:
			associations[lemmed] =  assoc['mi_norm']
	return associations

def relevance(job):
	text = job[1] + ' ' + job[2]
	for element in job:
		if '{' in element:
			obj =  ast.literal_eval(element)
			for ele in obj:
				data = obj[ele]['data']
				for thing in data:
					final = thing['data']
					if 'text' in final:
						add = final['text'].rstrip()
						add = filter(lambda x: x in string.printable, add)
						text += add.encode('utf-8')
	tokens = nltk.word_tokenize(text)
	filteredTokens = []
	for token in tokens:
		if re.search('[a-zA-Z]', token):
			token = token.lower()
			token = re.sub('[\\\.\/\*]','',token)
			try:
				if token and token not in stop:
					filteredTokens.append(lemming(token))
			except:
				print 'ERROR: ', token
	return filteredTokens

def leanDown(dictionary):
	parsed2 = {}
	parsed = dict(dictionary)
	for key in parsed:
		lemDown = lemming(key)
		if lemDown != key:
			if lemDown in parsed:
				parsed2[lemDown] = max(parsed[lemDown], parsed[key])
			else:
				parsed2[lemDown] = parsed[key]
		else:
			parsed2[key] = parsed[key]
	sorted_associations = sorted(parsed2.items(), key=operator.itemgetter(1))
	sorted_associations.reverse()
	return sorted_associations

def prettyPrint(dictionary):
	for tup in dictionary:
		print str(dictionary.index(tup)+1) + '. ' + tup[0] + ': ' + str(tup[1])

def printName(dictionary):
	dictionary = dictionary[:100]
	print ''
	prettyPrint(dictionary)
	user_input = raw_input("Add a word and its score in the following format -> word:score [Enter 's' to skip]: \n")
	if not user_input:
		return printName(dictionary)
	elif user_input == 's':
		return dictionary
	else:
		tup = user_input.split(':')
		word = lemming(tup[0].strip())
		score = float(tup[1].strip())
		dictionary = dict(dictionary)
		dictionary[word] = score
		sorted_associations = sorted(dictionary.items(), key=operator.itemgetter(1))
		sorted_associations.reverse()
		return printName(sorted_associations)

for career in careers:
	name = career[2].lower()
	filteredName = [i for i in name.split() if i not in stop]
	if len(career) < 4:
		associations = {}
		if len(filteredName) == 1:
			associations = getAssoc(filteredName[0])
		else:
			for word in filteredName:
				associations.update(getAssoc(word))
			joined = '%20'.join(filteredName)
			associations.update(getAssoc(joined))
		for entry in associations:
			associations[entry] = float(associations[entry])
		sorted_associations = sorted(associations.items(), key=operator.itemgetter(1))
		career.append(sorted_associations)
		print career
	else:
		career[3] = ast.literal_eval(career[3])
		dictionary =  dict(career[3])
		for word in filteredName:
			dictionary[word] = 0.9
		if len(filteredName) > 1:
			dictionary[name] = 1
		for entry in dictionary:
			dictionary[entry] = float(dictionary[entry])
		sorted_associations = sorted(dictionary.items(), key=operator.itemgetter(1))
		sorted_associations.reverse()
		print name
		sorted_associations = leanDown(sorted_associations)
		user_command = raw_input("y to arrange")
		if user_command == 'y':
			sorted_associations = printName(sorted_associations)
		career[3] = sorted_associations


with open('./careers.csv', 'wb') as careersfile:
	writer = csv.writer(careersfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	writer.writerow(['Code','Shorthand','Career', 'Associations'])
	for row in careers:
		writer.writerow(row)

for job in jobs[:10]:
	tokens = relevance(job)
	scores = {}
	for career in careers:
		scores[career[2]] = 0
		for token in tokens:
			if token in dict(career[3]):
				scores[career[2]] += float(dict(career[3])[token])
	print job, max(scores.items(), key=operator.itemgetter(1))