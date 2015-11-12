import urllib2

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
req = urllib2.Request('http://www.google.com')
response = urllib2.urlopen(req)
page_source = response.read()

print page_source