import psycopg2, json, sys, urllib2, re

if len(sys.argv)>1:
	arg = sys.argv[1]

with open('keys.json') as data_file:
	keys = json.load(data_file)
	host = keys[arg]['host']
	db = keys[arg]['database']
	user = keys[arg]['user']
	password = keys[arg]['password']

url = 'http://www.localhost:5000/api/job'
string = "dbname=" + db + " user=" + user + " host=" + host + " password=" + password
conn = psycopg2.connect(string)
cur = conn.cursor()
cur.execute("SELECT \"id\", \"title\",\"department\",\"intro\", \"description\", \"descriptionV2\" FROM \"Jobs\";")
rows = cur.fetchall()
for row in rows[:200]:
	id = row[0]
	title = row[1]
	department = row[2]
	intro = row[3]
	description = row[4]
	descriptionV2 = row[5]
	jd = {}
	if bool(intro):
		jd["intro"] = intro
	if bool(description):
		jd["description"] = re.sub("<.*?>", " ", description)
	if bool(descriptionV2):
		jd["descriptionV2"] = descriptionV2
	data = json.dumps({
		"title": title,
		"department": department,
		"jd": jd
	})
	req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
	f = urllib2.urlopen(req)
	response = f.read()
	print response
	f.close()
cur.close()
conn.close()