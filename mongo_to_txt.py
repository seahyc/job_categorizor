from pymongo import MongoClient
client = MongoClient()

db = client.jobstreet

collections = db.collection_names(include_system_collections=False)
for collection in  collections:

	mass_print = (entry for entry in db[collection].find())

	with open('./stores/' +collection + '.txt', 'w') as f:
		for jd in mass_print:
			f.write(jd['jd'].encode('utf-8') + '\n')