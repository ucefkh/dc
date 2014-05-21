from dc import db
from werkzeug import generate_password_hash, check_password_hash
import datetime

TEACHER = 0
STUDENT = 1

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	surname = db.Column(db.String(110))
	lastname = db.Column(db.String(80))
	email = db.Column(db.String(120), unique = True)
	role = db.Column(db.SmallInteger, default = STUDENT)
	pwdhash = db.Column(db.String(54))
	lastseen = db.Column(db.String(80))
	subjects = db.relationship('Subject', backref = 'author', lazy = 'dynamic')

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

class Subject(db.Model):

	id = db.Column(db.Integer, primary_key = True)
	subject_name = db.Column(db.String(140), unique = True)
	subject_des = db.Column(db.Text)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	topics = db.relationship('Topic', backref = 'topic', lazy = 'dynamic')

	def __repr__(self):
		# return '<Subject %r>' % (self.subject_name)
		return self.subject_name

class Topic(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	topic_name = db.Column(db.String(140), unique = True)
	topic_des = db.Column(db.Text)
	subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
	concepts = db.relationship('Concept', backref = 'concept', lazy = 'dynamic')

	def __repr__(self):
		return self.topic_name
		#return '<Topic %r>' % (self.topic_name)

class Concept(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	concept_name = db.Column(db.String(140), unique = True)
	concept_des = db.Column(db.Text)
	topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
	slides = db.relationship('Slide', backref = 'slides', lazy = 'dynamic')

	def __repr__(self):
		return self.concept_name
		#return '<Concept %r>' % (self.concept_name)

class Slide(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	slide_name = db.Column(db.String(140), unique = True)
	slide_text = db.Column(db.Text)
	# Add some for custom shiz
	concept_id = db.Column(db.Integer, db.ForeignKey('concept.id'))

	def __repr__(self):
		return self.slide_name
		#return '<Slide %r>' % (self.slide_name)

	