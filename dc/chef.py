from flask import render_template, redirect, url_for, request, session
from dc import dc, db, models
from forms import SignupForm, LoginForm
from models import User
from sessions import SignUp, SignIn
import outbound
import time


#################
# Error Routes  #
#################

@dc.errorhandler(404)
def internal_error(error):
    return "404 Error", 404

@dc.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return "Error 500", 500

################
# Test Routes  #
################

@dc.route("/test-out")
def test_mail():
    outbound.mailhandler.SendMail("arsalan.b4@gmail.com")

    return "Sent"


######################
# Session Management #
######################

@dc.route("/")
def home():
    return render_template("home.html")

@dc.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':
        code = SignUp(form, form.name.data, form.email.data, form.password.data)
        if code == 0:
            email = session['email']
            outbound.mailhandler.SendMail(email)
            return render_template('profile.html', email = email)
        elif code == 1:
            return render_template('profile.html', e)
    elif request.method == 'GET':
        return render_template('signup.html', form = form)

@dc.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        code = SignIn(form, form.email.data, form.password.data) 

        if code == 0:
            return render_template("profile.html", email = session['email'])          
    elif request.method == 'GET':
        return render_template('login.html', form=form)

@dc.route('/logout')
def logout():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    session.pop('email', None)
    return redirect(url_for('home'))

###

@dc.route("/feed", methods = ['GET', 'POST'])
def feed():
    from twitter import *
    x = []
    a = []
    auth = OAuth(
    consumer_key='works',
    consumer_secret='works',
    token='works',
    token_secret='works')

    t = Twitter(auth=auth)
    iterator = t.statuses.home_timeline(count=10)
    
    for tweet in iterator:
        x.append(tweet)

    for i in x:
        a.append(i["text"])

    return str(a)
