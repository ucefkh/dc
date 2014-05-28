from dc import models, db
from models import User
from flask import session, render_template

def SignUp(form, name, email, password):
    if form.validate_on_submit():
        if form.password.data == form.repassword.data:
            user = models.User(fullname = name, email = email, password = password)
            db.session.add(user)
            db.session.commit()

            session['email'] = user.email
            return render_template('profile.html', email = session['email']) 

        else:
            return "Password Mismatch"

    else:
        form.email.errors.append("Error")
        return render_template('signup.html', form = form)

def SignIn(form, email, password):
    if form.email.data not in session:
        if form.validate_on_submit():
            user = User.query.filter_by(email = form.email.data.lower()).first()                
            if user and user.check_password(form.password.data):
                session['email'] = user.email

                user.lastseen = time.strftime("%Y-%m-%d")
                db.session.commit()

                return render_template("profile.html", email = session['email'])
            else:
                form.email.errors.append("Invalid e-mail or password")
                return render_template('login.html', form = form)

def DeleteUser():
	
	# perm scripts here

	pass
		
		
		