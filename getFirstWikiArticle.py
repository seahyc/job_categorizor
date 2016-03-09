import requests, sys

def search (searchTerm):
    s = requests.get('https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srenablerewrites=true&srsearch=' + searchTerm)
    j = s.json()
    try:
        return search(j['query']['searchinfo']['suggestion'])
    except KeyError:
        r = j['query']['search']
        if len(r) >= 0:
            return get1st(r[0])

def get1st (searchResults):
    title = searchResults['title'].replace(' ', '+')
    s2 = requests.get('https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles=' + title)
    j2 = s2.json()
    extract = j2['query']['pages'].itervalues().next()['extract']
    return extract

print search(sys.argv[1])