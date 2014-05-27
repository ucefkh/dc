from flask.ext.wtf import Form
from wtforms import TextField, validators, ValidationError, PasswordField
from wtforms.validators import Required
from models import db, User

class SignupForm(Form):
	name = TextField("Full name",  [validators.Required("Please enter your first name.")])
	email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
	password = PasswordField('Password', [validators.Required("Please enter a password.")])
	repassword = PasswordField('Repeat Password', [validators.Required("Please enter password again.")])

	def get_id(self):
		return unicode(self.id)	
	
	def __repr__(self):
		return '<Name %r>' % (self.name)


"""

This script declares the datatypes of the input taken by the forms, handles the requirements and 
most of the front-end validation of the forms. 

We import the User model from the models.py script and the DB file, to enforce superimposition of data points 
between the two. 

"""