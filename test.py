# from flask import json
# from flask.json import jsonify
import requests

base = 'http://127.0.0.1:5000'

data = {
	"name": "aditya",
	"dob": "01/01/2021",
	"email": "email@example.com",
	"phoneNumber": "343434343"	
}

response = requests.post(base + '/', data)
print(response)