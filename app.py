#!/usr/local/bin/python

from flask import Flask, jsonify, request, abort, make_response
import analyze
from pprint import pprint

app = Flask(__name__)

weightage = {'title': 4.5,
			'department': 5,
			'jd': 6,
			'naive': 2,
			'keyword': 3.5,
			'lsi': 5,
			'tfidf': 4.5}


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

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
		weight = request.json['weightage']
	else:
		weight = weightage

	# try:
	# 	tabulate.append({'element': 'title'     , 'method': 'tfidf'  , 'result': analyze.title_tfidf(title)})
	# except:
	# 	print 'SEGFAULT'
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
	app.run(debug=True)
