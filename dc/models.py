from dc import db
from werkzeug import generate_password_hash, check_password_hash
import datetime
import hashlib, uuid

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(110))
	lastname = db.Column(db.String(80))
	email = db.Column(db.String(120), unique = True)
	pwdhash = db.Column(db.String(54))
	lastseen = db.Column(db.String(80))

	def __init__(self, fullname, email, password):
		self.set_name(fullname)
		self.email = email
		self.set_password(password)

	def set_name(self, fullname):
		for i in fullname:
			if i != " ":
				try:
					int(i)
				except ValueError:
					pass
				else:
					raise Exception("Invalid Input")	
		try:
			self.firstname, self.lastname = fullname.split(" ")
		except ValueError:
			self.firstname = fullname
			self.lastname = None

	def set_password(self, password):
		salt = uuid.uuid4().hex
		self.pwdhash = generate_password_hash(password + salt)

	def check_password(self, password):
		salt = uuid.uuid4().hex
		return check_password_hash(self.pwdhash, password + salt)

	def __repr__(self):
		return '<User %r>' % (self.surname)