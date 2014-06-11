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

@dc.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        rec = Photo(filename=filename, user=g.user.id)
        rec.store()
        flash("Photo saved.")
        return redirect(url_for('show', id=rec.id))
    return render_template('upload.html')

@dc.route('/photo/<id>')
def show(id):
    photo = Photo.load(id)
    if photo is None:
        abort(404)
    url = photos.url(photo.filename)
    return render_template('show.html', url=url, photo=photo)

##############

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


@dc.route("/feed", methods = ['GET', 'POST'])
def feed():
    return render_template("feed.html")