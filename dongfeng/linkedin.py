from bs4 import BeautifulSoup
from urllib import urlencode
import urllib2, time

prefix = 'https://bing.com/?q='
suffix = '+site%3Alinkedin.com%2Fcompany'
googleAppScript = 'https://script.google.com/macros/s/AKfycbzqg9Bs70bO8AXNfRfe803elnhxXk3BtsqAOXwcOB2ZY2d6MeI/exec'

textlist = {
    'basicDescription': 'div.basic-info-description p',
    'fullName': 'div.left-entity div h1 span',
    'industry': 'p.industry',
    'size': 'p.company-size',
    'address': 'div.basic-info-about ul li.vcard.hq p',
    'type': 'div.basic-info-about ul li.type p',
    'specialties': 'div.basic-info-about div p',
    'foundedYear': 'div.basic-info-about ul li.founded p'
}

imagelist = {
    'banner': '#content div.top-image img',
    'logo': 'div.top-bar.with-wide-image.with-nav.big-logo img'
}

websitelist = {
    'website': 'div.basic-info-about ul li.website p a'
}

fullist = {
    'text': textlist,
    'src' : imagelist,
    'href': websitelist
}

def bingscan(company):
    linkedinurl = getbinglink([prefix, company.replace(' ', '+'), suffix])
    return scan(linkedinurl)

def scan(linkedinurl):
    soup = getlinkedinpage(linkedinurl)
    co = {}
    for a,b in fullist.iteritems():
        for k,v in b.iteritems():
            co[k] = parseanattribute(soup, v, a)
    return co

def parseanattribute(soup, selector, attribute):
    target = soup.select(selector)[0]
    if attribute == 'text':
        return getattr(target, attribute)
    else:
        return target[attribute]

def getlinkedinpage(linkedinurl):
    data = urlencode({
        'url': linkedinurl
    })
    request = urllib2.Request(googleAppScript, data)
    html = urllib2.urlopen(request).read()
    return BeautifulSoup(html, 'html.parser')

def getbingfirstpage(query):
    try:
        return BeautifulSoup(urllib2.urlopen(query).read())
    except urllib2.URLError:
        time.sleep(10)
        return getbingfirstpage(query)

def getbinglink(querylist):
    select = 'li.b_algo h2 a'
    query = ''.join(querylist)
    soup = getbingfirstpage(query)
    selector = soup.select(select)
    if len(selector) > 0:
        return selector[0]['href']
    else:
        raise LookupError(1, 'Company linkedIn page not found')