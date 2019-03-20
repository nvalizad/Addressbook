from addressbook import *
import requests
import unittest

#POST test: needs some repairs
payload = {
	'name' : 'bob'
}
headers = {'content-type': 'application/json'}
r = requests.post('http://localhost:5000/people', data = payload, headers=headers)
assert(r.status_code == 200)

#GET test
r = requests.get('http://localhost:5000/people/bob')
assert(r.status_code == 200)
print("All tests passing\n")
exit()

#TEST CASES TO ADD:
#	*POST with all fields filled out
#	*DELETE with a name not in the server
#	*GET with querysearchquery
#	*PUT with invalid fields
