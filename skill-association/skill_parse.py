import csv, requests, pymongo, json, psycopg2, pprint
from pymongo import MongoClient

with open ('keys.json') as data_file:
        keys = json.load(data_file)
mongoKeys = keys['mongo']
client = MongoClient(mongoKeys['host'], mongoKeys['port'])
client['dongfeng'].authenticate(mongoKeys['username'], mongoKeys['password'], mechanism='SCRAM-SHA-1')
db = client['dongfeng']
skillsdb = db['skills']


# Update from csv to mongoDB
# with open('skills.csv', 'rb') as csvfile:
# 	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
# 	reader.next()
# 	for row in reader:
# 		skill = {}
# 		skill['id'] = row[0]
# 		skill['name'] = row[1]
# 		if not bool(skillsdb.find_one({'name':skill['name']})):
# 			print 'Adding ' + skill['name']
# 			skillsdb.update_one({'name':skill['name']}, {'$set': skill}, upsert=True)
# 		else:
# 			print 'Ignore ' + skill['name']

skills = skillsdb.find()

# Get abstract from duckduckgo
# for row in skills:
# 	if 'abstract' not in row.keys():
# 		skill = row['name'].replace(' ', '+').replace('.','')
# 		response = requests.get('http://api.duckduckgo.com/?format=json&q=' + skill).json()
# 		related = [{'url': topic['FirstURL'], 'text': topic['Text']} for topic in response['RelatedTopics'] if 'FirstURL' in topic.keys()]
# 		info = {
# 			'related': related,
# 			'abstract': response['Abstract'],
# 			'abstractUrl': response['AbstractURL']
# 		}
# 		print row, info
# 		skillsdb.update_one(row, {'$set': info}, upsert=True)
# 	else:
# 		print 'Skipping ' + row['name']

# Index skills into elasticsearch
# for row in skills:
# 	index = {
# 		'name': row['name'],
# 		'abstract': row['abstract'],
# 		'related': ' '.join([topic['text'] for topic in row['related'][:4]])
# 	}
# 	print index['name']
# 	r = requests.put('http://elasticsearch-241ecd0b-1.9caada87.cont.dockerapp.io:9200/dongfeng/skills/' + row['id'], data = json.dumps(index))
# 	print r

productionKeys = keys['production']

try:
	conn = psycopg2.connect("host='" + productionKeys['host'] + "'" + "dbname='" + productionKeys['database'] + "' user='" + productionKeys['user'] + "' password=" + productionKeys['password'])
except Exception as e:
	print e

cur = conn.cursor()

def fetch(resource, parameters):
	attributes = ', '.join(['"' + item + '"' for item in parameters])
	try:
		cur.execute('SELECT ' + attributes + ' from "' + resource + '"')
	except 	Exception as e:
		print e

	return cur.fetchall()

# jobs = fetch('Jobs', ['id', 'title', 'intro','descriptionV2'])

def V2Wrangler(v2, final):
	if type(v2) is list:
		for elem in v2:
			if (type(elem) is list or type(elem) is dict):
				final = V2Wrangler(elem, final)
	elif type(v2) is dict:
		for key in v2:
			if key == 'text':
				final.append(v2[key].replace('\\','').replace('\n','').replace('**',' ').replace('_', ''))
			elif (type(v2[key]) is list or type(v2[key]) is dict):
				final = V2Wrangler(v2[key], final)
	return final

# job_dump = []

# for job in jobs:
# 	# v2 = ' '.join(V2Wrangler(job[3], []))
# 	title = job[1] if job[1] else ''
# 	intro = job[2] if job[2] else ''
# 	jobText = ' '.join([title, intro])
# 	query = {
# 			  "query": {
# 			    "match": {
# 			      "_all": {
# 			        "query": jobText
# 			      }
# 			    }
# 			  }
# 			}
# 	r2 = requests.post('http://elasticsearch-241ecd0b-1.9caada87.cont.dockerapp.io:9200/dongfeng/skills/_search', data = json.dumps(query))
# 	response = r2.json()
# 	skill_list = [int(skill['_id']) for skill in response['hits']['hits']]
# 	job_dump.append({
# 		'JobId': job[0],
# 		'SkillsIds':  skill_list
# 	})

# with open('./jobSkill.json','w') as outfile:
# 	json.dump(job_dump, outfile, indent=4)

# resources = fetch('Resources', ['id', 'title', 'description'])
# resource_dump = []


# for res in resources:
# 	title = res[1].decode('utf-8') if res[1] else ''
# 	description = json.loads(res[2])['description'] if res[2] else ''
# 	resText = ' '.join([title, description])
# 	query = {
# 			  "query": {
# 			    "match": {
# 			      "_all": {
# 			        "query": resText
# 			      }
# 			    }
# 			  }
# 			}
# 	r2 = requests.post('http://elasticsearch-241ecd0b-1.9caada87.cont.dockerapp.io:9200/dongfeng/skills/_search', data = json.dumps(query))
# 	response = r2.json()
# 	skill_list = [int(skill['_id']) for skill in response['hits']['hits']]
# 	resource_dump.append({
# 		'ResourceId': res[0],
# 		'SkillsIds':  skill_list
# 	})

# with open('./resourceSkill.json','w') as outfile:
# 	json.dump(resource_dump, outfile, indent=4)

# professions = fetch('Professions', ['id', 'name', 'overview'])
# professions_dump = []

# for res in professions:
# 	title = res[1] if res[1] else ''
# 	description = res[2] if res[2] else ''
# 	resText = ' '.join([title, description])[:7100]
# 	query = {
# 			  "query": {
# 			    "match": {
# 			      "_all": {
# 			        "query": resText
# 			      }
# 			    }
# 			  }
# 			}
# 	r2 = requests.post('http://elasticsearch-241ecd0b-1.9caada87.cont.dockerapp.io:9200/dongfeng/skills/_search', data = json.dumps(query))
# 	response = r2.json()
# 	skill_list = [int(skill['_id']) for skill in response['hits']['hits']]
# 	professions_dump.append({
# 		'ProfessionId': res[0],
# 		'SkillsIds':  skill_list
# 	})

# with open('./professionSkill.json','w') as outfile:
# 	json.dump(professions_dump, outfile, indent=4)

