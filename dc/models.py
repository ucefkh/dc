from dc import db
from werkzeug import generate_password_hash, check_password_hash
import datetime
import hashlib, uuid

########################
## UTI Algorithm (tm) ##
########################

##############################
#     User Trust Indexing    #
##############################

unverified = 0 
verified = 1

class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(255), unique = True)
	firstname = db.Column(db.String(255))
	lastname = db.Column(db.String(255))
	email = db.Column(db.String(255), unique = True)
	image_location = db.Column(db.String(255))
	cover_location = db.Column(db.String(255))
	user_level = db.Column(db.String(255))
	pwdhash = db.Column(db.String(255))
	lastseen = db.Column(db.String(255))
	salt = db.Column(db.String(255))
	
	information = db.relationship('Information', backref = 'user', lazy = 'dynamic')
	threads = db.relationship('MessageThread', backref = 'messaged', lazy ='dynamic')
	posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
	projects = db.relationship('Project', backref = 'project_admin', lazy = 'dynamic')
	publicfriends = db.relationship('publicFriend', backref = 'publicfriend', lazy = 'dynamic')
	privatefriends = db.relationship('privateFriend', backref = 'privatefriend', lazy = 'dynamic')

	def __init__(self, username, fullname, email, password):
		self.username = username
		self.set_name(fullname)
		self.email = email
		self.salt = uuid.uuid4().hex
		self.set_password(password + self.salt)
		self.set_defaults()


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
		self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
		salt = uuid.uuid4().hex
		return check_password_hash(self.pwdhash, password + self.salt)

	def set_defaults(self):
		self.image_location = "/static/default-avatar.png"
		self.cover_location = "/static/default-cover.png"
		self.lastseen = "now"
		self.user_level = unverified

	def __repr__(self):
		return '<User %r>' % (self.firstname)


class Post(db.Model):
	__tablename__ = 'post'
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.String(255))
	timestamp = db.Column(db.DateTime)
	image = db.Column(db.String(255))

	writers = db.relationship('Writer', backref = 'who_wrote', lazy = 'dynamic')
	user_post_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post %r>' % (self.body)


class Writer(db.Model):
	__tablename__ = 'writer'
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(255))
	firstname = db.Column(db.String(255))
	lastname = db.Column(db.String(255))
	email = db.Column(db.String(255))
	image_location = db.Column(db.String(255))
	cover_location = db.Column(db.String(255))

	post_writer_id = db.Column(db.Integer, db.ForeignKey('post.id'))

	def __repr__(self):
		return '<Writer %r>' % (self.username)

class publicFriend(db.Model):
	__tablename__ = 'publicfriend'
	id = db.Column(db.Integer, primary_key = True)
	username_friend = db.Column(db.String(255), unique = True)
	date_added = db.Column(db.String(255))	
	user_pubfriend_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<PubFriend %r>' % (self.username_friend)

class privateFriend(db.Model):
	__tablename__ = 'privatefriend'
	id = db.Column(db.Integer, primary_key = True)
	username_friend = db.Column(db.String(255), unique = True)
	date_added = db.Column(db.String(255))	
	user_privfriend_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<PrivFriend %r>' % (self.username_friend)

class MessageThread(db.Model):
	__tablename__ = "thread"
	id = db.Column(db.Integer, primary_key = True, unique = True)
	sender_u = db.Column(db.String(255), unique = True)
	sender_name = db.Column(db.String(255))
	sender_image = db.Column(db.String(255))
	messages = db.relationship('Message', backref = 'parentthread', lazy = 'dynamic')
	user_thread_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Message %r>' % (self.sender_u)

class Message(db.Model):
	__tablename__ = 'message'
	sender = db.Column(db.String(255))
	receiver = db.Column(db.String(255))
	id = db.Column(db.Integer, primary_key = True)
	date_sent = db.Column(db.Integer)
	text = db.Column(db.String(255))
	data_content = db.Column(db.String(255))	
	thread_message_id = db.Column(db.Integer, db.ForeignKey('thread.id'))
	

	def __repr__(self):
		return '<Message %r>' % (self.text)

class Information(db.Model):
	__tablename__ = 'information'
	id = db.Column(db.Integer, primary_key = True)

	job =db.Column(db.String(255))
	cv = db.Column(db.String(255))
	handle_twitter = db.Column(db.String(255), unique = True)
	hometown = db.Column(db.String(255))
	about_me = db.Column(db.String(255))
	rel_status = db.Column(db.String(255))
	gender = db.Column(db.String(255))

	paypal_email = db.Column(db.String(255))

	user_information_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Information %r>' % (self.hometown)

class Project(db.Model):
	__tablename__ = 'project'
	id = db.Column(db.Integer, primary_key = True)
	project_name = db.Column(db.String(255))
	author = db.Column(db.String(255))
	project_desc = db.Column(db.String(255))
	image = db.Column(db.String(255))
	project_tasks = db.relationship('ProjectTask', backref = 'project', lazy = 'dynamic')
	user_project_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Project %r' % (self.project_name)

class ProjectTask(db.Model):
	__tablename__ = 'projecttask'
	id = db.Column(db.Integer, primary_key = True)
	tasktext = db.Column(db.String(255))
	image = db.Column(db.String(255))
	task_author = db.Column(db.String(255))
	assigned_to = db.Column(db.String(255))
	due_date = db.Column(db.String(255))
	taskconvo = db.relationship('ProjectConvo', backref = 'projecttask', lazy = 'dynamic')
	project_task_id = db.Column(db.Integer, db.ForeignKey('project.id'))

	def __repr__(self):
		return '<Task %r>' % (self.tasktext)

class ProjectConvo(db.Model):
	__tablename__ = "projectconvo"
	id = db.Column(db.Integer, primary_key = True)
	poster_u = db.Column(db.String(255))
	poster_im = db.Column(db.String(255))
	post_text = db.Column(db.String(255))
	project_convo_id = db.Column(db.Integer, db.ForeignKey('projecttask.id'))

	def __repr__(self):
		return '<Convo %r>' % (self.post_text)	 
		

		
		
