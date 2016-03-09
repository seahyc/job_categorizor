import csv, urllib2, time
from bs4 import BeautifulSoup

prefix = 'http://www.bing.com/search?q='
suffix = '+%28site%3Acareerplanning.about.com+OR+site%3Amyplan.com%29'
read_list = []

def getFirstPage(query):
    try:
        return urllib2.urlopen(query)
    except urllib2.URLError:
        time.sleep(10)
        return getFirstPage(query)

def getLink(select, querylist):
    query = ''.join(querylist)
    response = getFirstPage(query)
    soup = BeautifulSoup(response.read())
    selector = soup.select(select)
    if len(selector) > 0:
        return selector[0]['href']
    else:
        return "Empty"

if __name__ == '__main__':
    with open('job_codes.csv', 'rUb') as csvfile:
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            read_list.append(row)

    for row in read_list:
        joint = ' '.join(row)
        profession = joint.split(',')[0].strip()
        page = getLink('li.b_algo h2 a', [prefix, profession.replace(' ', '+'), suffix])
        row.pop()
        row.append(page)
        print row

    read_list2 = []

    with open('job_codes2.csv', 'rUb') as csvfile:
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            profession = row[0]
            url = row[2]
            if 'myplan' not in url and  'careerplanning' not in url:
                print row
                # row[2] = getLink('li.b_algo h2 a', [prefix, profession.replace(' ', '+'), suffix])
            read_list2.append(row)

    # with open('job_codes2.csv', 'wb') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(['title', 'category','url'])
    #     for row in read_list2:
    #         writer.writerow(row)