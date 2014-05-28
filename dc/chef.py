from flask import render_template, redirect, url_for, request, session
from dc import dc, db, models
from forms import SignupForm, LoginForm
from models import User
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
        
    
    elif request.method == 'GET':
        return render_template('signup.html', form = form)

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

                    return render_template("profile.html", email = session['email'])
                else:
                    form.email.errors.append("Invalid e-mail or password")
                    return render_template('login.html', form=form)            
    elif request.method == 'GET':
        return render_template('login.html', form=form)