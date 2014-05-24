from flask import render_template, redirect, url_for
from dc import dc, db, models
from models import User


################
# Test Routes  #
################

@dc.route("/")
def test():
    return "Dreams Collective"

