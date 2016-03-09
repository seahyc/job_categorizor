import csv, urllib2, json, operator, string
from bs4 import BeautifulSoup

read_list = []

# with open('job_codes2.csv', 'Urb') as infile:
#     reader = csv.reader(infile)
#     reader.next()
#     for row in reader:
#         save = {
#             'profession' : row[0],
#             'career' : row[1],
#             'source' : row[2]
#         }
#         read_list.append(save)

with open('profession_overview.json') as infile:
    read_list = json.load(infile)
    for item in read_list:
        if 'overview' in item:
            item['overview'] = [line.encode('utf-8') for line in item]

for save in read_list:
    if 'overview' in save and min(len(line) for line in save['overview']) < 20:
        print save
        if 'myplan.com/careers' in save['source']:
            response = urllib2.urlopen(save['source'])
            soup = BeautifulSoup(response.read())
            tags = [tag.text.encode('utf-8').strip() for tag in soup.select('span.tool_description')]
            max_id, max_val = max(enumerate([len(tag) for tag in tags[:8]]), key=operator.itemgetter(1))
            tag = tags[max_id]
            tag = filter(lambda x: x in string.printable, tag)
            save['overview'] = [tag]
        elif 'careerplanning.about.com' in save['source']:
            response = urllib2.urlopen(save['source'])
            soup = BeautifulSoup(response.read())
            tag = soup.select('div.col-push-2.content-responsive p')
            for id, para in enumerate(tag):
                if "Employment Facts" in para.text:
                    final = [filter(lambda x: x in string.printable, strip.text.encode('utf-8')) for strip in tag[2:id]]
            save['overview'] = final
        print save
        with open('profession_overview.json', 'w') as outfile:
            json.dump(read_list, outfile, sort_keys = True, indent=4, ensure_ascii=False)

# for row in read_list:
#     if 'overview' not in row:
#         print ''
#     elif min(len(line) for line in row['overview']) < 20:
#         print row['overview']