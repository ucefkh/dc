from flask import render_template, redirect, url_for
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
	return render_template("signup.html", form = form)