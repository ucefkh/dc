from flask.ext.wtf import Form
from wtforms import TextField, validators, ValidationError, PasswordField, FileField
from wtforms.validators import Required
from models import db, User

class SignupForm(Form):
	username = TextField("Username", [validators.Required("Find a unique username.")])
	name = TextField("Full name",  [validators.Required("Please enter your first name.")])
	email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
	password = PasswordField('Password', [validators.Required("Please enter a password.")])
	repassword = PasswordField('Repeat Password', [validators.Required("Please enter password again.")])

	def get_id(self):
		return unicode(self.id)	
	
	def __repr__(self):
		return '<Name %r>' % (self.name)

class LoginForm(Form):
	email = TextField("email", validators = [Required()])
	password = PasswordField('Password', [validators.Required("Please enter a password.")])

class PostForm(Form):
	content = TextField("What's on your mind?", [validators.Required("Required!")])
	image = FileField()
		
class UploadForm(Form):
	profile_pic = FileField("Profile")
	cover_pic = FileField("Cover Photo")

class MessageForm(Form):
	message = TextField("Enter your text here...")
	username = TextField("Username")
	message_image = FileField("Message Image")	


"""class ProjectForm(Form):
	job = TextField("Where do you work?")
	handle_twitter = TextField("Enter your text here...")
	hometown = TextField("Where are you from?")
	about_me = TextField("Tell us about yourself...")
	rel_status = TextField("What's your relationship status?")
	paypal_email = TextField("What's your Paypal ID?")
	cv = FileField("Upload your CV here")	"""

class InfoForm(Form):
	job = TextField("Where do you work?")
	handle_twitter = TextField("Enter your text here...")
	hometown = TextField("Where are you from?")
	about_me = TextField("Tell us about yourself...")
	rel_status = TextField("What's your relationship status?")
	paypal_email = TextField("What's your Paypal ID?")
	cv = FileField("Upload your CV here")
	gender = TextField("What's your gender?")

class ConvoForm(Form):
	message = TextField("Enter your text here...")
	message_image = FileField("Message Image")	


"""
This script declares the datatypes of the input taken by the forms, handles the requirements and 
most of the front-end validation of the forms. 
We import the User model from the models.py script and the DB file, to enforce superimposition of data points 
between the two. 
"""

print "Forms have been built."
