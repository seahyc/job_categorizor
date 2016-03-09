pg = require('pg')
jsonfile = require('jsonfile')
await = require('await')
fs = require('fs')
parse = require('csv-parse')
prettyjson = require('prettyjson')
postConnect = await('close-client')
industries = []

rs = fs.createReadStream('./industry.csv')
parser = parse {columns: true}

parser.on 'readable', ->
	while data = parser.read()
		industries.push data

parser.on 'error', (err) ->
	console.log err.message

rs.pipe parser

rs.on 'end', ->
	if process.argv.length > 2
		arg = process.argv[2]
	else
		throw new Error "Specify production or staging database"

	file = './companies.json'
	try
		companies = jsonfile.readFileSync file
	catch e
		companies = []

	ids = (co['id'] for co in companies)
	keys = require('./keys.json')
	host = keys[arg]['host']
	db = keys[arg]['database']
	user = keys[arg]['user']
	password = keys[arg]['password']

	conString = "postgres://" + user + ":" + password + "@" + host + "/" + db
	client = new pg.Client conString

	client.connect (err) ->
		if err
			postConnect.fail err
			return console.error('Error fetching client from pool', err)
		client.query "SELECT \"id\", \"name\", \"tagline\", \"description\", \"descriptionV2\", \"website\" FROM \"Companies\" ORDER BY \"id\";", (err, result) ->
			if err
				postConnect.fail err
				return console.error('Error running query', err)
			for row in result.rows
				if row['id'] not in ids
					console.log row['name']
					companies.push row
			jsonfile.writeFileSync file, companies, {spaces: 4}
			client.end()
			postConnect.keep 'close-client', companies
			return
		return

	postConnect.then (get) ->
		companies = get['close-client']
		for co in companies
			if !!co['descriptionV2']
				co['descriptionV3'] = (datum['data']['text'] for datum in co['descriptionV2']['data']).join()