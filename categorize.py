import psycopg2, json, sys, requests, re
from pprint import pprint

if len(sys.argv)>1:
	arg = sys.argv[1]

with open('keys.json') as data_file:
	keys = json.load(data_file)
	host = keys[arg]['host']
	db = keys[arg]['database']
	user = keys[arg]['user']
	password = keys[arg]['password']

url = 'http://localhost:5000/api/job'
string = "dbname=" + db + " user=" + user + " host=" + host + " password=" + password
conn = psycopg2.connect(string)
cur = conn.cursor()
cur.execute("SELECT \"id\", \"title\",\"department\",\"intro\", \"description\", \"descriptionV2\" FROM \"Jobs\";")
rows = cur.fetchall()

for row in rows:
	id = row[0]
	with open('data.json', 'r') as infile:
		try:
			feeds = json.load(infile)['data']
		except:
			feeds = []
	id_list = [item['jobId'] for item in feeds]
	if id in id_list:
		print 'PASS!'
		continue
	title = row[1].decode('utf-8')
	department = row[2]
	intro = row[3]
	description = row[4]
	descriptionV2 = row[5]
	jd = {}
	if bool(intro):
		intro = intro.decode('utf-8')
		jd["intro"] = intro
	if bool(description):
		jd["description"] = re.sub("<.*?>", " ", description)
	if bool(descriptionV2):
		jd["descriptionV2"] = descriptionV2
	data = {
		"title": title,
		"jd": "json.dumps(jd)",
		"weightage": json.dumps(
			{'title': 55,
			'department': 50,
			'jd': 75,
			'naive': 20,
			'keyword': 35,
			'lsi': 70,
			'tfidf': 45
			})
	}
	if bool(department):
		department = department.decode('utf-8')
		data["department"] = department
	data = json.dumps(data)
	headers = {'Content-Type': 'application/json'}
	r = requests.post(url, data = data, headers=headers)
	resp = r.json()['data']
	top = resp[0]
	print str(id) + ': ' + title + '/' + str(department) + '--->' +top['career']
	entry = {"jobId": id, "career": top['career'], "title": title}
	feeds.append(entry)
	with open('data.json', 'w') as outfile:
		obj = {'data':feeds}
		json.dump(obj, outfile, indent=4)
cur.close()
conn.close()