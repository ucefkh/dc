from flask import render_template, redirect, url_for, request, session
from dc import dc, db, models
from forms import SignupForm, LoginForm
from models import User
from sessions import SignUp, SignIn
import time


################
# Test Routes  #
################

@dc.route("/")
def test():
    return render_template("index.html")

@dc.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':
        code = SignUp(form, form.name.data, form.email.data, form.password.data)
        if code == 0:
            return render_template('profile.html', email = session['email'])
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