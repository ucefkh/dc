# Make Imports Here

def SignUp(self, form, name, email, password):
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

def SignIn():
	pass

def DeleteUser():
	
	# perm scripts here

	pass
		
		
		