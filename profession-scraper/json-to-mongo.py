import pymongo, json, scrape_url, urllib2, re
import collections
from pymongo import MongoClient
from bs4 import BeautifulSoup

client = MongoClient('localhost', 27017)
professions = client.professions
i = raw_input('1) json-mongo\n2) mongo-json\n3) supplement\n')

def json_mongo():
    fileinput = raw_input('Which json file to read? [profession_overview.json]') or 'profession_overview.json'
    print 'Reading ' + fileinput + '...'
    with open(fileinput) as infile:
        import_list = json.load(infile)
    for row in import_list:
        career = row['career']
        profession = row['profession']
        careers = professions[career]
        careers.update_one({'profession': profession}, {'$set': row}, upsert=True)
        professions.all.update_one({'profession': profession}, {'$set': row}, upsert=True)

def mongo_json():
    textRegex = re.compile('\r\n')
    dump_list = []
    fileoutput = raw_input('Name of output file? [profession_overview2.json]') or 'profession_overview2.json'
    print 'Dumping to ' + fileoutput + '...'
    careers = professions.collection_names()
    careers.pop()
    for career in careers:
        for profession in professions[career].find():
            profession['overview'] = [re.sub(textRegex, '', p).strip().encode('utf-8') for p in profession['overview']]
            orderedDict = collections.OrderedDict()
            keys = ['profession', 'career', 'source', 'overview']
            for key in keys:
                if key in profession:
                    orderedDict[key] = profession[key]
            dump_list.append(orderedDict)
    with open(fileoutput, 'w') as outfile:
        json.dump(dump_list, outfile, indent=4, encoding="utf-8", ensure_ascii=False)

def supplement():
    prefix = 'http://www.bing.com/search?q='
    suffix = '+site%3Apayscale.com%2Fresearch'
    for entry in professions.all.find():
        del entry['_id']
        if len(entry['overview']) < 10:
            print entry['overview']
            original_len =len(''.join(entry['overview']))
            profession = entry['profession']
            url = scrape_url.getLink('li.b_algo h2 a', [prefix, profession.replace(' ', '+'), suffix])
            response = urllib2.urlopen(url)
            soup = BeautifulSoup(response.read())
            tags = soup.select('div.panel-default div.panel-heading h3')
            new_length = 0
            for tag in tags:
                if 'Job Description' in tag.text:
                    body = tag.find_next('div')
                    list = body.find_all('p') if len(body.find_all('p'))>0 else body.find_all('li')
                    textRegex = re.compile('\r\n')
                    entry['overview'] = [re.sub(textRegex, '', li.text).strip() for li in list]
                    new_length = len(''.join(entry['overview']))
            if new_length >= original_len:
                print entry['overview']
                print ''
                entry['source'] = url
                career = entry['career']
                careers = professions[career]
                careers.update_one({'profession': profession}, {'$set': entry}, upsert=True)
                professions.all.update_one({'profession': profession}, {'$set': entry}, upsert=True)


def error():
    print 'Wrong option dude!'

options = {
    '1': json_mongo,
    '2': mongo_json,
    '3': supplement
}

options.get(i, error)()