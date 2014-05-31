from flask import render_template, redirect, url_for, request, session
from dc import dc, db, models
from forms import SignupForm, LoginForm
from models import User
from sessions import SignUp, SignIn
import time


################
# Test Routes  #
################

@dc.route("/test-out")
def test_mail():
    import smtplib
     
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
     
    sender = 'dev.dreamscollective@gmail.com'
    recipient = 'mail@arsalanbashir.com'
    subject = 'Gmail SMTP Test'
    body = 'Test'
     
    """Sends an e-mail to the specified recipient."""
     
    body = "" + body + ""
     
    headers = ["From: " + sender,
               "Subject: " + subject,
               "To: " + recipient,
               "MIME-Version: 1.0",
               "Content-Type: text/html"]
    headers = "\r\n".join(headers)
     
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
     
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(sender, "1Q2W3e4r_")
     
    session.sendmail(sender, recipient, headers + "\r\n\r\n" + body)
    session.quit()
    return "Sent an email"

@dc.route("/")
def home():
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