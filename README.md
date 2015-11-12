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
            
#### Sample Post Request

*curl Post Request*

`curl -H "Content-Type: application/json" -X POST -d '{"title":"Web Developer", "jd": "Develop javascript webapps"}' http://dongfeng.glints.com/api/job`

*response*

`{
  "data": [
    {
      "career": "Business Development",
      "reference": {
        "department_keyword": "0.0",
        "department_naive": "0.0",
        "jd_keyword": "2.282301",
        "jd_lsi": "0.806659720838",
        "jd_tfidf": "0.85094056651",
        "title_keyword": "2.6605215",
        "title_lsi": "11.7916479707",
        "title_naive": "0.0"
      },
      "relevance": "100.000487701"
    },
    {
      "career": "Marketing",
      "reference": {
        "department_keyword": "0.0",
        "department_naive": "0.0",
        "jd_keyword": "8.82492513",
        "jd_lsi": "1.26733750105",
        "jd_tfidf": "0.357426018454",
        "title_keyword": "0.0",
        "title_lsi": "7.6347912848",
        "title_naive": "0.0"
      },
      "relevance": "62.0988603508"
    },
    {
      "career": "Engineering",
      "reference": {
        "department_keyword": "0.0",
        "department_naive": "0.0",
        "jd_keyword": "0.0",
        "jd_lsi": "-0.214049317874",
        "jd_tfidf": "0.454233353958",
        "title_keyword": "0.0",
        "title_lsi": "7.93948620558",
        "title_naive": "0.0"
      },
      "relevance": "7.3373977676"
    },
    {
      "career": "Consulting",
      "reference": {
        "department_keyword": "0.0",
        "department_naive": "0.0",
        "jd_keyword": "0.0",
        "jd_lsi": "-0.170870739967",
        "jd_tfidf": "0.42455538176",
        "title_keyword": "0.0",
        "title_lsi": "4.71650697291",
        "title_naive": "0.0"
      },
      "relevance": "4.07381731376"
    },
    {
      "career": "Real Estate",
      "reference": {
        "department_keyword": "0.0",
        "department_naive": "0.0",
        "jd_keyword": "0.0",
        "jd_lsi": "-0.0686160195619",
        "jd_tfidf": "0.329489763826",
        "title_keyword": "1.390977",
        "title_lsi": "4.02851466089",
        "title_naive": "0.0"
      },
      "relevance": "3.75620247469"
    },
    {
      "career": "Information Technology",
      "reference": {
        "department_keyword": "0.0",
        "department_naive": "0.0",
        "jd_keyword": "0.0",
        "jd_lsi": "0.0824373168871",
        "jd_tfidf": "1.20548209548",
        "title_keyword": "0.0",
        "title_lsi": "17.6702038944",
        "title_naive": "0.0"
      },
      "relevance": "3.57244328403"
    },
    {
      "career": "Program & Product Management",
      "reference": {
        "department_keyword": "0.0",
        "department_naive": "0.0",
        "jd_keyword": "0.0",
        "jd_lsi": "-0.0251044845209",
        "jd_tfidf": "0.0",
        "title_keyword": "0.0",
        "title_lsi": "0.96159523353",
        "title_naive": "0.0"
      },
      "relevance": "1.95605376468"
    },
    {
      "career": "Product Management",
      "reference": {
        "department_keyword": "0.0",
        "department_naive": "0.0",
        "jd_keyword": "0.0",
        "jd_lsi": "-0.0996096432209",
        "jd_tfidf": "0.307115689851",
        "title_keyword": "0.0",
        "title_lsi": "2.94130202383",
        "title_naive": "0.0"
      },
      "relevance": "1.83748111282"
    },
    {
      "career": "Sales",
      "reference": {
        "department_keyword": "0.0",
        "department_naive": "0.0",
        "jd_keyword": "0.0",
        "jd_lsi": "0.313218478113",
        "jd_tfidf": "0.432498961687",
        "title_keyword": "0.0",
        "title_lsi": "5.70421166718",
        "title_naive": "0.0"
      },
      "relevance": "1.57177066108"
    },
    {
      "career": "Art and Design",
      "reference": {
        "department_keyword": "0.0",
        "department_naive": "0.0",
        "jd_keyword": "0.0",
        "jd_lsi": "0.043607671978",
        "jd_tfidf": "1.1030561775",
        "title_keyword": "0.0",
        "title_lsi": "10.6540795416",
        "title_naive": "0.0"
      },
      "relevance": "1.04223764586"
    },
    {
      "career": "Legal",
      "reference": {
        "department_keyword": "0.0",
        "department_naive": "0.0",
        "jd_keyword": "0.0",
        "jd_lsi": "0.0",
        "jd_tfidf": "0.0",
        "title_keyword": "0.0",
        "title_lsi": "0.446097585373",
        "title_naive": "0.0"
      },
      "relevance": "0.907170395515"
    },
    {
      "career": "Media & Communications",
      "reference": {
        "department_keyword": "0.0",
        "department_naive": "0.0",
        "jd_keyword": "0.0",
        "jd_lsi": "0.0779810920358",
        "jd_tfidf": "0.753715636209",
        "title_keyword": "0.0",
        "title_lsi": "7.43663705885",
        "title_naive": "0.0"
      },
      "relevance": "0.888847885598"
    },
    {
      "career": "Community & Social Services",
      "reference": {
        "department_keyword": "0.0",
        "department_naive": "0.0",
        "jd_keyword": "0.0",
        "jd_lsi": "0.293912021443",
        "jd_tfidf": "0.353113126941",
        "title_keyword": "0.0",
        "title_lsi": "3.00849035382",
        "title_naive": "0.0"
      },
      "relevance": "0.634797557053"
    },
    {
      "career": "Research",
      "reference": {
        "department_keyword": "0.0",
        "department_naive": "0.0",
        "jd_keyword": "0.0",
        "jd_lsi": "-0.115115940571",
        "jd_tfidf": "0.0973278013989",
        "title_keyword": "0.0",
        "title_lsi": "2.14672710747",
        "title_naive": "0.0"
      },
      "relevance": "0.424618044801"
    },
    {
      "career": "Accounting",
      "reference": {
        "department_keyword": "0.0",
        "department_naive": "0.0",
        "jd_keyword": "0.0",
        "jd_lsi": "0.216271081008",
        "jd_tfidf": "0.0",
        "title_keyword": "0.0",
        "title_lsi": "0.68178689573",
        "title_naive": "0.0"
      },
      "relevance": "0.299513582464"
    },
    {
      "career": "Purchasing",
      "reference": {
        "department_keyword": "0.0",
        "department_naive": "0.0",
        "jd_keyword": "0.0",
        "jd_lsi": "0.104743831325",
        "jd_tfidf": "0.350276364014",
        "title_keyword": "0.0",
        "title_lsi": "3.94566927105",
        "title_naive": "0.0"
      },
      "relevance": "0.294046359921"
    },
    {
      "career": "Quality Assurance",
      "reference": {
        "department_keyword": "0.0",
        "department_naive": "0.0",
        "jd_keyword": "0.0",
        "jd_lsi": "0.0",
        "jd_tfidf": "0.0491639231332",
        "title_keyword": "0.0",
        "title_lsi": "2.5792468898",
        "title_naive": "0.0"
      },
      "relevance": "0.25750740623"
    },
    {
      "career": "Education",
      "reference": {
        "department_keyword": "0.0",
        "department_naive": "0.0",
        "jd_keyword": "0.0",
        "jd_lsi": "0.222571464255",
        "jd_tfidf": "0.322187324055",
        "title_keyword": "0.0",
        "title_lsi": "1.21105165221",
        "title_naive": "0.0"
      },
      "relevance": "0.176197230774"
    },
    {
      "career": "Operations",
      "reference": {
        "department_keyword": "0.0",
        "department_naive": "0.0",
        "jd_keyword": "0.0",
        "jd_lsi": "0.259445914999",
        "jd_tfidf": "0.112087176181",
        "title_keyword": "0.0",
        "title_lsi": "1.68156601489",
        "title_naive": "0.0"
      },
      "relevance": "0.0989940272796"
    },
    {
      "career": "Entrepreneurship",
      "reference": {
        "department_keyword": "0.0",
        "department_naive": "0.0",
        "jd_keyword": "0.0",
        "jd_lsi": "0.0",
        "jd_tfidf": "0.400731682777",
        "title_keyword": "0.102249",
        "title_lsi": "-4.16475813836e-07",
        "title_naive": "0.0"
      },
      "relevance": "0.0828660391136"
    },
    {
      "career": "Military & Protective Services",
      "reference": {
        "department_keyword": "0.0",
        "department_naive": "0.0",
        "jd_keyword": "0.0",
        "jd_lsi": "0.0226432818454",
        "jd_tfidf": "0.0",
        "title_keyword": "0.0",
        "title_lsi": "1.1217459105",
        "title_naive": "0.0"
      },
      "relevance": "0.0511767880169"
    },
    {
      "career": "Human Resources",
      "reference": {
        "department_keyword": "0.0",
        "department_naive": "0.0",
        "jd_keyword": "0.0",
        "jd_lsi": "-0.0157920399215",
        "jd_tfidf": "0.00961230500252",
        "title_keyword": "0.0",
        "title_lsi": "0.764319766313",
        "title_naive": "0.0"
      },
      "relevance": "0.0144440654075"
    },
    {
      "career": "Finance",
      "reference": {
        "department_keyword": "0.0",
        "department_naive": "0.0",
        "jd_keyword": "0.0",
        "jd_lsi": "0.333504695445",
        "jd_tfidf": "0.0229446238372",
        "title_keyword": "0.0",
        "title_lsi": "0.865974314511",
        "title_naive": "0.0"
      },
      "relevance": "0.0129784335233"
    },
    {
      "career": "Administrative",
      "reference": {
        "department_keyword": "0.0",
        "department_naive": "0.0",
        "jd_keyword": "0.0",
        "jd_lsi": "0.0424291344825",
        "jd_tfidf": "0.0320210934151",
        "title_keyword": "0.0",
        "title_lsi": "0.367463598959",
        "title_naive": "0.0"
      },
      "relevance": "0.000511191361777"
    },
    {
      "career": "Healthcare Services",
      "reference": {
        "department_keyword": "0.0",
        "department_naive": "0.0",
        "jd_keyword": "0.0",
        "jd_lsi": "0.0177284778329",
        "jd_tfidf": "0.0382667344529",
        "title_keyword": "0.0",
        "title_lsi": "0.718887839466",
        "title_naive": "0.0"
      },
      "relevance": "0.000487701384621"
    }
  ]
}`

#### Demo

For a demo, simply post to [http://dongfeng.glints.com/api/job](http://dongfeng.glints.com/api/job)