from flask import render_template, redirect, url_for, request, session
from dc import dc, db, models
from forms import SignupForm
from models import User


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
        if form.validate_on_submit():
            if form.password.data == form.repassword.data:
                item = models.User(fullname = form.name.data, email = form.email.data, password = form.password.data)
                db.session.add(item)
                db.session.commit()

                session['email'] = item.email
                return render_template('profile.html', email = session['email'])

            else:
                return "Password Mismatch"

        else:
            form.email.errors.append("Error")
            return render_template('signup.html', form = form)
    
    elif request.method == 'GET':
        return render_template('signup.html', form = form)