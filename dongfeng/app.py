from flask import Flask, jsonify, request, abort, make_response, render_template
from pymongo import MongoClient
from datetime import datetime, timedelta
import analyze, ast, sys, os, subprocess, json, linkedin
with open ('keys.json') as data_file:
	keys = json.load(data_file)['mongo']
client = MongoClient(keys['host'], keys['port'])
client['dongfeng'].authenticate(keys['username'], keys['password'], mechanism='SCRAM-SHA-1')
db = client['dongfeng']
companies = db['companies']

app = Flask(__name__)

weightage = {'title': 4.5,
			'department': 5,
			'jd': 6,
			'naive': 2,
			'keyword': 3.5,
			'lsi': 5,
			'tfidf': 4.5}

def searchCompany(companyName):
	return companies.find_one({'name': companyName.replace(' ', '+').lower()})

def checkCache(companyName):
	cachedCompany = searchCompany(companyName)
	if cachedCompany:
		del cachedCompany['_id']
		if 'industry' in cachedCompany:
			code = 0
			# {'message': 'Industry exists. Do not crawl.'}
		elif checkTimeDelta(cachedCompany) < timedelta(days=7):
			code = 1
			# {'message': 'Industry does not exist. Do not crawl.'}
		else:
			code = 2
			# {'message': 'Outdated, crawl again.'}
		return code, cachedCompany
	else:
		return 3, None
		# {'message': 'Uncached. Crawl.'}

def checkTimeDelta(companyObj):
	if 'updatedAt' in companyObj:
		return datetime.now() - companyObj['updatedAt']
	else:
		return checkTimeDelta(updateCache(companyObj['name'], {}))

def updateCache(companyName, updateObj):
	companyName = companyName.replace(' ', '+').lower()
	updateObj['updatedAt'] = datetime.utcnow()
	companies.update_one({'name': companyName}, {'$set': updateObj}, upsert=True)
	insert = searchCompany(companyName)
	del insert['_id']
	return insert

@app.errorhandler(400)
def not_found(error):
	return make_response(jsonify({'error': str(error)}), 400)

@app.route('/')
def root():
	return render_template('README.html')

@app.route('/api/company', methods=['POST'])
def casper():
	companyName = request.json['company'].replace(' ', '+')
	mongoCompany = checkCache(companyName)
	if mongoCompany[0] == 0:
		return jsonify({'data': mongoCompany[1]}), 200
	elif mongoCompany[0] == 1:
		return jsonify({'message': 'Company industry not available.'}), 404
	APP_ROOT = os.path.dirname(os.path.realpath(__file__))
	CASPER = 'casperjs'
	SCRIPT =  os.path.join(APP_ROOT, 'linkedin.coffee')
	params = CASPER + ' ' + SCRIPT + ' ' + companyName
	try:
		log = subprocess.check_output(params, shell=True)
		output = ast.literal_eval(log)
		insert = updateCache(output['name'], output)
		return jsonify({'data': insert}), 200
	except Exception, e:
		return make_response(jsonify({'error': str(e)}), 400)

@app.route('/api/job', methods=['POST'])
def get_tasks():
	if not request.json or not 'title' in request.json or not 'jd' in request.json:
		abort(400)
	title = request.json['title']
	jd = request.json['jd']
	department = ''
	tabulate = []
	if 'department' in request.json:
		department = request.json['department']
	if 'weightage' in request.json:
		weight = ast.literal_eval(request.json['weightage'])
	else:
		weight = weightage

	tabulate.append({'element': 'jd'        , 'method': 'tfidf'  , 'result': analyze.jd_tfidf(jd)})
	tabulate.append({'element': 'title'     , 'method': 'lsi'    , 'result': analyze.title_lsi(title)})
	tabulate.append({'element': 'jd'        , 'method': 'lsi'    , 'result': analyze.jd_lsi(jd)})
	tabulate.append({'element': 'department', 'method': 'naive'  , 'result': analyze.highestMatch(department)})
	tabulate.append({'element': 'title'     , 'method': 'naive'  , 'result': analyze.highestMatch(title)})
	tabulate.append({'element': 'department', 'method': 'keyword', 'result': analyze.keywordMatch(department)})
	tabulate.append({'element': 'title'     , 'method': 'keyword', 'result': analyze.keywordMatch(title)})
	tabulate.append({'element': 'jd'        , 'method': 'keyword', 'result': analyze.keywordMatch(jd)})
	return jsonify({'data': dec_to_string(weighting(tabulate, weight))}), 200

def dec_to_string(lst):
	lst = compress(lst)
	return [{'career':obj['career'], 'relevance':str(obj['relevance']), 'reference': obj['reference']} for obj in lst]

def compress(lst):
	lst1 = [d['relevance'] for d in lst]
	max1 = max(lst1)
	min1 = min(lst1)
	max2 = 100
	min2 = 0
	for d in lst:
		d['relevance'] = convert(d['relevance'], min1, max1, min2, max2)
	return lst

def convert(val, min1, max1, min2, max2):
	range1 = max1 - min1
	range2 = max2 - min2
	return (((val - min1) * range2)/ range1) + min1

def weighting(tabulate, weightage):
	master_list = [{'career': career['career'], 'relevance': 1, 'reference': {} } for career in tabulate[0]['result']]
	for tab in tabulate:
		weight = weightage[tab['element']] * weightage[tab['method']]
		for career in master_list:
			score = next((item['relevance'] for item in tab['result'] if (item['career'] == career['career'] and item['relevance'] > 0)), 0)
			if score != 0:
				career['relevance'] *= weight * score
			reference = [{tab['element']+ '_' + tab['method']:str(item['relevance'] * weight)} for item in tab['result'] if item['career'] == career['career']]
			career['reference'].update(reference[0])
	return sorted(master_list, key=lambda item: -item['relevance'])

if __name__ == "__main__":
	if len(sys.argv)>1:
		port = int(sys.argv[1])
	else:
		port = 5000
	app.run(host='0.0.0.0', port=port, debug=True)
