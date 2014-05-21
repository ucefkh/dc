from flask import render_template, flash, redirect, session, url_for, request, make_response
from dc import dc, db, models
from forms import LoginForm, SignupForm, AddSubject, AddConcept, CourseBuilder
from models import User, Subject
from hashlib import md5
import time




################
# Test Routes  #
################

@dc.route('/course')
def tster():
    return render_template("course.html")

################
# Home Routing #
################

@dc.route('/')
def home():
    return render_template('home.html')

###################
# Sign up Handler #
###################

@dc.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            if form.password.data == form.repassword.data:
                surname, lastname = form.name.data.split()

                item = models.User(surname = surname, lastname = lastname, email = form.email.data, password = form.password.data)
                db.session.add(item)
                db.session.commit()

                session['email'] = item.email
                return render_template('home.html')

            else:
                return "Password Mismatch"

        else:
            form.email.errors.append("Error")
            return render_template('signup.html', form = form)
    
    elif request.method == 'GET':
        return render_template('signup.html', form = form)

#################
# Login Handler #
#################

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

                    return redirect(url_for('home'))
                else:
                    form.email.errors.append("Invalid e-mail or password")
                    return render_template('login.html', form=form)            
    elif request.method == 'GET':
        return render_template('login.html', form=form)


####################
# Closing sessions #
####################  

@dc.route('/logout')
def logout():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    session.pop('email', None)
    return redirect(url_for('home'))

#################
# Teacher Views #
#################   

@dc.route('/teacher', methods=['GET', 'POST'])
def teacher_home():
    form = AddSubject()

    if 'email' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(email = session['email']).first()
    # The next line constructs a Gravatar URL. Should I store it in the database? What about changes? Maybe a constructor function in the DB model?
    avatar = 'http://www.gravatar.com/avatar/' + md5(user.email).hexdigest() + '?d=mm&s=' + str(100)
    subjects_show = user.subjects.all()

    fullname = user.surname + " " +user.lastname

    if request.method == 'GET':
        try:
            return render_template('teacher.html', user = fullname, lastseen = user.lastseen, avatar = avatar, subjects_show = subjects_show, form = form)
        except UnboundLocalError:
            return render_template('teacher.html', user = fullname, lastseen = user.lastseen, avatar = avatar, subjects_show = subjects_show, topic_id = 0, form = form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            add = models.Subject(subject_name = form.subject_name.data, subject_des = form.subject_des.data, author = user)
            db.session.add(add)
            db.session.commit()

            return redirect(url_for("teacher_home"))


@dc.route('/teacher/topic/<topic_id>', methods=['GET', 'POST'])
def concept_view(topic_id):
    form = AddSubject()

    if 'email' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(email = session['email']).first()
    avatar = 'http://www.gravatar.com/avatar/' + md5(user.email).hexdigest() + '?d=mm&s=' + str(100)
    
    bakref = models.Subject.query.get(topic_id)
    topics_show = models.Topic.query.filter_by(topic = bakref)

    fullname = user.surname + " " + user.lastname

    if request.method == 'GET':
        try:
            return render_template('hex.html', user = fullname, lastseen = user.lastseen, avatar = avatar, subjects_show = topics_show, form = form)
        except UnboundLocalError:
            return render_template('hex.html', user = fullname, lastseen = user.lastseen, avatar = avatar, subjects_show = topics_show, concept_id = 0, form = form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            add = models.Topic(topic_name = form.subject_name.data, topic_des = form.subject_des.data, topic = bakref)
            db.session.add(add)
            db.session.commit()

            return redirect(url_for("concept_view", topic_id = topic_id))

@dc.route('/teacher/concept/<concept_id>', methods=['GET', 'POST'])
def course_view(concept_id):
    form = AddConcept()

    if 'email' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(email = session['email']).first()
    # The next line constructs a Gravatar URL. Should I store it in the database? What about changes? Maybe a constructor function in the DB model?
    avatar = 'http://www.gravatar.com/avatar/' + md5(user.email).hexdigest() + '?d=mm&s=' + str(100)
    
    bakref = models.Topic.query.get(concept_id)
    concepts_show = models.Concept.query.filter_by(concept = bakref)

    fullname = user.surname + " " + user.lastname

    if request.method == 'GET':
        try:
            return render_template('concept.html', user = fullname, lastseen = user.lastseen, avatar = avatar, subjects_show = concepts_show, form = form)
        except UnboundLocalError:
            return render_template('concept.html', user = fullname, lastseen = user.lastseen, avatar = avatar, subjects_show = concepts_show, topic_id = 0, form = form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            add = models.Concept(concept_name = form.subject_name.data, concept_des = form.subject_des.data, concept = bakref)
            db.session.add(add)
            db.session.commit()

            return redirect(url_for("course_view", concept_id = concept_id))



@dc.route('/teacher/concept/edit/<concept_id>', methods=['GET', 'POST'])
def teacher_edit(concept_id):
    form = CourseBuilder()
    
    if 'email' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(email = session['email']).first()
    avatar = 'http://www.gravatar.com/avatar/' + md5(user.email).hexdigest() + '?d=mm&s=' + str(100)
    
    bakref = models.Concept.query.get(concept_id)
    slides_show = models.Slide.query.filter_by(slides = bakref)

    fullname = user.surname + " " + user.lastname

    if request.method == 'GET':
        return render_template('course.html', user = fullname, lastseen = user.lastseen, conceptname = bakref, slides_show = slides_show, avatar = avatar, form = form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            add = models.Slide(slide_name = form.slide_name.data, slide_text = form.slide_text.data, slides = bakref)
            db.session.add(add)
            db.session.commit()

            return redirect(url_for("teacher_edit", concept_id = concept_id))

@dc.route('/teacher/<name>/analytics')
def teacher_analytics(name):
	return render_template("analytics.html")

@dc.route('/teacher/<name>/new')
def make_new(name):
	return "this is a new course, yay"

#################
# Student Views #
#################

@dc.route('/student')
def student_home():
    if 'email' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(email = session['email']).first()
    avatar = 'http://www.gravatar.com/avatar/' + md5(user.email).hexdigest() + '?d=mm&s=' + str(100)

    if user is None:
        return redirect(url_for('login'))
    else:
        return render_template('student.html')

@dc.route('/student/<name>/insights')
def student_analytics():
    return render_template('student.html')

@dc.route('/student/<name>/courses')
def student_courses():
    return render_template('student.html')

@dc.route('/student/<name>/threads')
def student_threads():
    return render_template('student.html')

@dc.route('/student/<name>/settings')
def student_settings():
    return render_template('student.html')
