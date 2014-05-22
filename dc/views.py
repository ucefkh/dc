from flask import render_template, flash, redirect, session, url_for, request, make_response
from dc import dc, db, models
from forms import LoginForm, SignupForm
from models import User
from hashlib import md5
import time


################
# Test Routes  #
################

@dc.route('/home')
def tster():
    return render_template("course.html")

################
# Home Routing #
################

@dc.route('/')
def home():
    return render_template('home.html')

###################
# Sign up Handler #
###################

@dc.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            if form.password.data == form.repassword.data:
                surname, lastname = form.name.data.split()

                item = models.User(surname = surname, lastname = lastname, email = form.email.data, password = form.password.data)
                db.session.add(item)
                db.session.commit()

                session['email'] = item.email
                return render_template('home.html')

            else:
                return "Password Mismatch"

        else:
            form.email.errors.append("Error")
            return render_template('signup.html', form = form)
    
    elif request.method == 'GET':
        return render_template('signup.html', form = form)

#################
# Login Handler #
#################

@dc.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.email.data.lower() not in session:
            if form.validate_on_submit():
                user = User.query.filter_by(email = form.email.data.lower()).first()            
                if user and user.check_password(form.password.data):
                    session['email'] = user.email

                    user.lastseen = time.strftime("%Y-%m-%d")
                    db.session.commit()

                    return redirect(url_for('home'))
                else:
                    form.email.errors.append("Invalid e-mail or password")
                    return render_template('login.html', form=form)            
    elif request.method == 'GET':
        return render_template('login.html', form=form)


####################
# Closing sessions #
####################  

@dc.route('/logout')
def logout():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    session.pop('email', None)
    return redirect(url_for('home'))

#################
# Teacher Views #
#################   

@dc.route('/home', methods=['GET', 'POST'])
def teacher_home():
    return "Logged in"



