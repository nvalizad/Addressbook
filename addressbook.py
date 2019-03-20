import requests
from flask import *
from elasticsearch import Elasticsearch

app = Flask(__name__)

es = Elasticsearch()


@app.route('/people/?pageSize={<int:size>}&page={<int:num>}&query={<string:q>}')
def search(name, size, num, q):
		doc = {
		'from' : num, 'size' : size,
		'query': q

		}
		res = es.search(index= "people", body = doc)
		return jsonify(res)
#GET method: will find the person with the name and return their info
@app.route('/people/<string:name>', methods=['GET'])
def find(name):
	res = es.search(index="people", body={"query": {"prefix" : { "name" : name }}})
	total = res['hits']['total']
	#if total == 0:
	#for doc in res['hits']:
	#	if res['total'] == 0:
	#	abort(404)
		#print("%s) %s" % (doc['_id'], doc['_source']['name']))
	return jsonify(res)

#PUT method: will update the information of the person with the given name
@app.route('/people/<string:name>', methods=['PUT'])
def update(name):
	email = ""
	number = ""
	res = es.search(index="people", body={"query": {"prefix" : { "name" : name }}})
	for doc in res['hits']['hits']:
		email = doc['_source']['email']
		number = doc['_source']['number']

	doc = {
	'name' : name,
	'id' : request.json.get('id', ""),
	'email' : request.json.get('email', email),
	'number' : request.json.get('number', number),
	}
	res = es.index(index="people", doc_type='family', id=1, body=doc)
	print(res['result'])
	return jsonify(res)

#DELETE method: will delete the entry of the person with given name
@app.route('/people/<string:name>', methods=['DELETE'])
def remove(name):
	res = es.search(index="people", body={"query": {"prefix" : { "name" : name }}})
	for doc in res['hits']['hits']:
		num = doc['_id']
	res = es.delete(index = "people", doc_type = 'family', id=num)
	return jsonify(res)

#POST method: Will add a person into the address book. Note that when adding a person the only required field is the name
@app.route('/people', methods=['POST'])
def add():
	doc = {
	'name' : request.json['name'],
	'id' : request.json.get('id', ""),
	'email' : request.json.get('email', ""),
	'number' : request.json.get('number', ""),
	}
	res = es.index(index="people", doc_type='family', id=1, body=doc)
	print(res['result'])
	return jsonify(res)


#To test, run elasticsearch on one terminal, and issue curl requests with http://localhost:5000
#Port can be configured to your requirements
app.run(port=8080, debug=True)