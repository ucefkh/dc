from dc import db
from werkzeug import generate_password_hash, check_password_hash
import datetime

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	surname = db.Column(db.String(110))
	lastname = db.Column(db.String(80))
	email = db.Column(db.String(120), unique = True)
	pwdhash = db.Column(db.String(54))
	lastseen = db.Column(db.String(80))

	def __init__(self, surname, lastname, email, password):
		self.surname = surname.title()
		self.lastname = lastname.title()
		self.email = email.lower()
		self.set_password(password)

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)

	def __repr__(self):
		return '<User %r>' % (self.surname)