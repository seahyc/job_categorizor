### Dong Feng

#### Intro

Dong Feng is a job categorizor. Based on a corpus of job descriptions and job titles, it'll infer the career/industry of a query job description. The corpuscraper is a scrapy spider that collects the corpus and stores it in a mongo database.

Based on the gensim NLP library, the corpus and the query are both converted into the LSI and tf-idf vector space, from which similarity is inferred. 

#### Getting Started

To get started, simply run the app like so

`./app.py` in your terminal

This will run a Flask api server on your localhost at port 80. 

#### Usage

To get the category inference, send a post request to [http://localhost:80/api/job](http://localhost:80/api/job) with the header of `Content-Type: application/json` and a json object containing the following keys:

- title (job title)
- jd (job description)
- department (optional)
- weightage (optional)

Every field should be a string, except for weightage. For jd, it can be a json object, converted to a string. The app will parse it accordingly and discard the keys. Of course, it can also be a string.

Weightage should be a dictionary. Because the app uses several similarity querying systems, for different values, the weightage system is implemented to adjust their respective influence. The default weightage is as follows:

`weightage = {'title': 4.5,
			'department': 5,
			'jd': 6,
			'naive': 2,
			'keyword': 3.5,
			'lsi': 5,
			'tfidf': 4.5}`
            
#### Demo

For a demo, simply post to [http://dongfeng.glints.com/api/job](http://dongfeng.glints.com/api/job)
