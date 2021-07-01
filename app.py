# from operator import index
import os

# import smtplib for the actual sending function
import smtplib

# import the email modules
from email.message import EmailMessage
# from typing_extensions import Required
import phonenumbers

from flask import Flask, jsonify, request, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))

# configuring app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# init marshmallow
ma = Marshmallow(app)

# Models
class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True)
	dob = db.Column(db.String)
	email = db.Column(db.String)
	phoneNumber = db.Column(db.String)

	def __init__(self, name, dob, email, phoneNumber):
		self.name = name
		self.dob = dob
		self.email = email
		self.phoneNumber = phoneNumber

# users schema
class UserSchema(ma.Schema):
	class Meta:
		fields = ('id', 'name', 'dob', 'email', 'phoneNumber')

# init schema
user_schema = UserSchema(many=True)

@app.route('/', methods=['POST'])
def addUser():
	print(request.json)
	phoneNumber = request.json['phoneNumber']
	dob = request.json['dob']
	name = request.json['name']
	email = request.json['email']

	try:
	 	p = phonenumbers.parse(phoneNumber)
	 	if not phonenumbers.is_valid_number(p):
	 		return 'value error', 400
	except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
		return 'Invalid Phone Number', 400

	new_user = Users(name, dob, email, phoneNumber)
	db.session.add(new_user)
	db.session.commit()
	
	# smtp stuff
	s = smtplib.SMTP(host='smtp.ethereal.email', port='587')
	s.starttls()
	s.login(user='reyna.walker67@ethereal.email', password='jFh2jB3zmDMtEwDPjq')

	msg = EmailMessage()
	msg.set_content('Long time no see!')
	msg['Subject'] = 'hello'
	msg['From'] = 'Jimmy <jimmy@jimmy.com>'
	msg['To'] = f'{email}'
	
	s.send_message(msg)
	s.quit()
	return 'hello', 200

@app.route('/users', methods=['GET'])
def getAllUsers():
	# querying database
	all_users = Users.query.all()
	# print(all_users)
	# serializer
	result = user_schema.dump(all_users) 
	return jsonify(result)
