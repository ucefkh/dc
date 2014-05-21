from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField, validators, ValidationError, PasswordField, RadioField
from wtforms.validators import Required
from models import db, User

class LoginForm(Form):
	email = TextField("email", validators = [Required()])
	password = PasswordField('Password', [validators.Required("Please enter a password.")])

class AddSubject(Form):
	subject_name = TextField("subject_name", validators = [Required()])
	subject_des = TextField("subject_des")

class AddConcept(Form):
	subject_name = TextField("subject_name", validators = [Required()])
	subject_des = TextField("subject_des")

class SignupForm(Form):
	name = TextField("Full name",  [validators.Required("Please enter your first name.")])
	email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
	password = PasswordField('Password', [validators.Required("Please enter a password.")])
	repassword = PasswordField('Repeat Password', [validators.Required("Please enter password again.")])

	def get_id(self):
		return unicode(self.id)	
	
	def __repr__(self):
		return '<Name %r>' % (self.name)

class CourseBuilder(Form):
	slide_name = TextField("Enter a title",  [validators.Required("This is kinda required")])
	slide_text = TextField("Type your text here")
		
