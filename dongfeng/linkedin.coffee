start = new Date().getTime()

casper = require('casper').create(
    verbose: false,
    logLevel: 'debug',
    pageSettings: {
     loadImages:  false,
     loadPlugins: false
    })

casper.options.onResourceRequested = (casper, requestData, request) ->
    skip = [
        'radar',
        'static',
        'cedexis'
    ]
    skip.forEach (needle) ->
        if requestData.url.indexOf(needle) > 0
            request.abort()

company = {}
company['name'] = casper.cli.args[0]
keys = require './keys.json'
username = keys['linkedin']['username']
password = keys['linkedin']['password']

scrapeLinkedIn = (company) ->
    company['basicDescription'] = @fetchText '#content div.basic-info-description p'
    company['fullName'] = @fetchText('#body div.top-bar.with-wide-image.with-nav.big-logo div.header div.left-entity div h1 span')
    company['industry'] = @fetchText('#body div.top-bar.with-wide-image.with-nav.big-logo div.header div.left-entity div p.industry')
    company['size'] = @fetchText '#body div.top-bar.with-wide-image.with-nav.big-logo div.header div.left-entity div p.company-size'
    company['address'] = @fetchText 'div.basic-info-about ul li.vcard.hq p'
    company['website'] = @fetchText 'div.basic-info-about ul li.website p a'
    company['type'] = @fetchText 'div.basic-info-about ul li.type p'
    company['specialties'] = @fetchText 'div.basic-info-about div p'
    company['foundedYear'] = @fetchText 'div.basic-info-about ul li.founded p'
    company['banner'] = @getElementAttribute('#content div.top-image img', 'src')
    company['logo'] = @getElementAttribute('div.top-bar.with-wide-image.with-nav.big-logo img', 'src')
    company['linkedinPage'] = @getCurrentUrl()
    return company

casper.start()

# LinkedIn search

###url = 'https://www.linkedin.com'

casper.thenOpen url, ->
    # LinkedIn Login
    @fillXPath 'form.login-form',
        '//input[@name="session_key"]' : username
        '//input[@name="session_password"]' : password, true

    @then ->
        if !@exists '#control_gen_2 p strong'
            @thenOpen url + '/vsearch/c?type=companies&keywords=' + company['name'], ->
                @thenClick '#results li.mod.result.idx0.company div h3 a', ->
                    company = scrapeLinkedIn.call casper,company
        else###

# Bing search
url2 = 'https://bing.com/?q='
suffix = '+site%3Alinkedin.com%2Fcompany'
googleAppScript = 'https://script.google.com/macros/s/AKfycbzqg9Bs70bO8AXNfRfe803elnhxXk3BtsqAOXwcOB2ZY2d6MeI/exec'

casper.thenOpen url2 + company['name'] + suffix, ->
    if @exists 'li.b_algo h2 a'
        linkedinUrl = @getElementAttribute('li.b_algo h2 a', 'href');
        @thenOpen googleAppScript, {
          method: 'POST',
          data:
            'url': linkedinUrl
        }, (response) ->
          if response.status == 200
            if @page.content.exists '#body div.top-bar.with-wide-image.with-nav.big-logo div.header div.left-entity div h1 span'
              company = scrapeLinkedIn.call casper,company
    else
        # DuckDuckGo Search
        url3 = 'http://www.duckduckgo.com/search?q='
        casper.thenOpen url3 + company['name'] + suffix, ->
            @thenClick 'a.result__url:nth-of-type(1)', ->
                if @exists '#body div.top-bar.with-wide-image.with-nav.big-logo div.header div.left-entity div h1 span'
                    company = scrapeLinkedIn.call casper,company
    @then ->
        for k, v of company
            if k == 'linkedinPage'
                company[k] = v.split('?')[0]
            else if v
                company[k] = v.replace(/\n/g, ' ').replace(/'/g, "\'").trim()
            else
                company[k] = ""
casper.run ->
    console.log JSON.stringify company
    end = new Date().getTime()
    # console.log end-start
    @exit()