from flask import render_template, redirect, url_for, request, session, jsonify, g
from dc import dc, db, models 
from forms import SignupForm, LoginForm, PostForm, UploadForm, MessageForm, InfoForm
from models import User, Information
from sessions import SignUp, SignIn, login_required
import outbound, time, datetime
from werkzeug import secure_filename


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

@dc.route("/test", methods=['GET', 'POST'])
def test_mail():
    user = User.query.filter_by(email = session['email']).first()
    return models.Friend.query.filter_by(friend = user)

@dc.route("/settings", methods=['GET', 'POST'])
def settings():
    return "Settings page for %s" % session['email']

######################
# Session Management #
######################

@dc.route("/", methods=['GET', 'POST'])
def home():
    signup_form = SignupForm()
    login_form = LoginForm()

    if request.method == 'GET':
        try:
            if session['email'] == "":
                return render_template("home.html", form = signup_form, log = login_form)
            else:
                try:
                    user = User.query.filter_by(email = session['email']).first()
                    username = user.username
                    return redirect(url_for('profile', username = username))
                except:
                    return render_template("home.html", form = signup_form, log = login_form)
        except KeyError:
            return render_template("home.html", form = signup_form, log = login_form)
    elif request.method == 'POST':
        if request.form['btn'] == 'Sign Up':
            form = signup_form
            code = SignUp(form, form.username.data,form.name.data, form.email.data, form.password.data)
            if code == 0:
                email = session['email']
                # outbound.mailhandler.SendMail(email)
                user = User.query.filter_by(email = session['email']).first()
                return redirect(url_for('profile', username = user.username))
            elif code == 1:
                user = User.query.filter_by(email = session['email']).first()
                return redirect(url_for('profile', username = user.username)) 
        else:
            if login_form.email.data =="" or login_form.password.data =="":
                return render_template('home.html', log = login_form, form = signup_form)
            else:
                code = SignIn(login_form, login_form.email.data, login_form.password.data) 
                if code == 0:
                    user = User.query.filter_by(email = session['email']).first()
                    return redirect(url_for('profile', username = user.username))
                elif code == 1:
                    login_form.email.errors.append("Invalid e-mail or password")
                    return render_template('home.html', log = login_form, form = signup_form)


@dc.route("/signup", methods=['GET', 'POST'])
def signup():
    if 1 < 2:
    #faux test condition
        form = SignupForm()

        if request.method == 'POST':
            code = SignUp(form, form.username.data,form.name.data, form.email.data, form.password.data)
            if code == 0:
                email = session['email']
                # outbound.mailhandler.SendMail(email)
                user = User.query.filter_by(email = session['email']).first()
                return redirect(url_for('profile', username = user.username))
            elif code == 1:
                user = User.query.filter_by(email = session['email']).first()
                return redirect(url_for('profile', username = user.username))  
        elif request.method == 'GET':
            return render_template('signup.html', form = form)
    else:
        return "Not Public Yet"

@dc.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        code = SignIn(form, form.email.data, form.password.data) 
        if code == 0:
            user = User.query.filter_by(email = session['email']).first()
            return redirect(url_for('profile', username = user.username))
        elif code == 1:
            form.email.errors.append("Invalid e-mail/username or password")
            return render_template('home.html', form = form)
    elif request.method == 'GET':
        return render_template('home.html', form=form)

@dc.route('/logout')
def logout():
    if 'email' not in session:
        return redirect(url_for('login'))
        
    session.pop('email', None)
    return redirect(url_for('home'))

####################################
##  Settings and Profile Editting ##
####################################


@dc.route('/edit', methods = ['GET', 'POST'])
def edit():
    form = InfoForm()
    user = User.query.filter_by(email = session['email']).first()

    PATH = "../dc/dc/static/uploads/%s/" % user.username

    if request.method == 'GET':
        return render_template('edit.html', user = user, form = form)
    elif request.method == 'POST':

        #######################
        ## Manual Validation ##
        #######################

        if form.job.data == None or form.job.data == "":
            job = "None"
        else:
            job = form.job.data

        if form.handle_twitter.data == None or form.handle_twitter.data == "":
            handle_twitter = "None"
        else:
            handle_twitter = form.handle_twitter.data

        if form.paypal_email.data == None or form.paypal_email.data == "":
            paypal_email = "None"
            user.user_level = 0
            db.session.commit()
        else:
            paypal_email = form.paypal_email.data

        if form.hometown.data == None or form.hometown.data == "":
            hometown = "None"
        else:
            hometown = form.hometown.data

        if form.about_me.data == None or form.about_me.data == "":
            about_me = "None"
        else:
            about_me = form.about_me.data

        if form.gender.data == None or form.gender.data == "":
            gender = "None"
        else:
            gender = form.gender.data

        if form.rel_status.data == None or form.rel_status.data == "":
            rel_status = "None"
        else:
            rel_status = form.rel_status.data

        if len(form.cv.data) < 1:
            cv_path = None
        else:
            filename = secure_filename(form.cv.data.filename)
            cv_path = PATH + filename
            form.cv.data.save(PATH+filename)

        #########################

        first_info = models.Information(job = job, cv = cv_path, handle_twitter = handle_twitter, paypal_email = paypal_email, hometown = hometown, about_me = about_me, rel_status = rel_status, gender = gender, user = user)
    
        db.session.add(first_info)
        db.session.commit()
        return redirect(url_for('profile', username = user.username))
#######################
##  Profile Routing  ##
#######################

@dc.route('/<username>', methods = ['GET', 'POST'])
def profile(username):
    user = User.query.filter_by(username = username).first()

    pubs = []
    privs = []

    pub_fr = models.publicFriend.query.filter_by(publicfriend = User.query.filter_by(email = session['email']).first())
    pri_fr = models.privateFriend.query.filter_by(privatefriend = User.query.filter_by(email = session['email']).first())

    for i in pub_fr:
        pubs.append(i.username_friend)
    for i in pri_fr:
        privs.append(i.username_friend)

    if username in pubs:
        pubdisplay_code = True

    if username in privs:
        privdisplay_code = True

    if user != None:
        if login_required(username):
            poster = PostForm()
            edit = UploadForm()

            PATH = "../dc/dc/static/uploads/%s/" % username
            REF_PATH = "/static/uploads/%s/" % username

            if user is None:
                return redirect(url_for("home"))

            if request.method == 'POST':
                if edit.profile_pic.data == "" and edit.cover_pic.data == "":
                    try:
                        filename = secure_filename(poster.image.data.filename)
                        poster.image.data.save(PATH+filename)
                    except:
                        filename = None

                    if len(poster.content.data) < 1 and filename == None:
                        return redirect(url_for('profile', username = username))
                    else:
                        post = models.Post(body = poster.content.data, timestamp = datetime.datetime.utcnow(), image= filename, author = user)
                        writer = models.Writer(username = user.username, firstname = user.firstname, lastname = user.lastname, email = user.email, image_location = user.image_location, cover_location = user.cover_location, who_wrote = post)
                        db.session.add(post)
                        db.session.add(writer)
                        db.session.commit()
                        return render_template("profile.html", user = user, form = poster, edit = edit)
                elif poster.content.data == "" and poster.image.data == "":
                    try:
                        name_cover = secure_filename(edit.cover_pic.data.filename)
                        name_profile = secure_filename(edit.profile_pic.data.filename)
                        edit.cover_pic.data.save(PATH+name_cover)
                        edit.profile_pic.data.save(PATH+name_profile)      
                        user.image_location = REF_PATH + name_profile
                        user.cover_location = REF_PATH + name_cover
                        db.session.commit()
                    except:
                        return redirect(url_for('profile', username = username))
                    return render_template("profile.html", user = user, form = poster, edit = edit)
                else:
                    return "Wait. What?"

            elif request.method == 'GET':
                return render_template("profile.html", user = user, form = poster, edit = edit)
        else:
            message = MessageForm()

            PATH = "../dc/dc/static/uploads/%s/" % username

            poster = PostForm()
            user = User.query.filter_by(username = username).first()

            try:
                filename = secure_filename(poster.image.data.filename)
                poster.image.data.save(PATH+filename)
            except:
                filename = None

            try:
                if len(session['email']) > 0:
                    visitor = User.query.filter_by(email = session['email']).first()
                    post_ability = True
                else:
                    visitor = None
                    post_ability = False
            except KeyError:
                visitor = None
                post_ability = False

            if request.method == 'POST':
                if message.message.data == "" and message.message_image.data == "":
                    post = models.Post(body = poster.content.data, timestamp = datetime.datetime.utcnow(), image= filename, author = user)
                    temp_writer = models.Writer(username = visitor.username, firstname = visitor.firstname, lastname = visitor.lastname, email = visitor.email, image_location = visitor.image_location, cover_location = visitor.cover_location, who_wrote = post)
                    db.session.add(post)
                    db.session.add(temp_writer)
                    db.session.commit()

                    return render_template("p-profile.html", user = user, form = poster, message = message, post_ability = post_ability, pubs = pubdisplay_code, privs = privdisplay_code) 
                elif poster.content.data == "" and poster.image.data == "":
                    try:
                        message_filename = secure_filename(message.message_image.data.filename)
                        message.message_image.data.save(PATH+filename)
                    except:
                        message_filename = None
                    mess = models.Message(sender = visitor.username, receiver = user.username,text = message.message.data, data_content = message_filename, date_sent = datetime.datetime.utcnow())
                    db.session.add(mess)
                    db.session.commit()
                    #~ return render_template("p-profile.html", user = user, form = poster, message = message, post_ability = post_ability, pubs = pubdisplay_code, privs = privdisplay_code)
                    return render_template("p-profile.html", user = user, form = poster, message = message, post_ability = post_ability)
            elif request.method == 'GET':
                return render_template("p-profile.html", user = user, form = poster, message = message,  post_ability = post_ability) 
    else:
        return "No such user"

############
## Events ##
############

#@socketio.on('addpub')
@dc.route('/<username>/add-public')
def add_public(username):
    user = User.query.filter_by(email = session['email']).first()    
    friend = models.publicFriend(username_friend = username, date_added = datetime.datetime.utcnow(), publicfriend = user)
    db.session.add(friend)
    db.session.commit()
    print "Added to Public Network"
    return redirect(url_for('profile', username = username))

#@socketio.on('addpriv')
@dc.route('/<username>/add-private')
def add_private(username):
    user = User.query.filter_by(email = session['email']).first()    
    friend = models.privateFriend(username_friend = username, date_added = datetime.datetime.utcnow(), privatefriend = user)
    db.session.add(friend)
    db.session.commit()
    print "Added to Private Network"
    return redirect(url_for('profile', username = username))


###############################
## Feed and Machine Learning ##
###############################

@dc.route('/feed')
def feed_view():
    user = User.query.filter_by(email = session['email']).first()
    publicfriends = models.publicFriend.query.filter_by(publicfriend = user)

    feed_maker = []

    for friend in publicfriends:
        for post in models.Post.query.filter_by(author = friend):
            feed_maker.append(post)

    return render_template('feed.html', user = user, feed = feed_maker)

#############################
## Messaging and Threading ##
#############################

@dc.route('/<username>/messages')
def message(username):
    user = User.query.filter_by(email = session['email']).first()
    #~ rmessages = models.Message.query.filter_by(sender = username).group_by(models.Message.sender)
    #~ rmessages = models.Message.query.filter_by(sender = username).group_by(models.Message.sender)
    rmessages = models.Message.query.filter_by(sender = username)
    smessages = models.Message.query.filter_by(receiver = username)
    return render_template('message.html', rmessages = rmessages, smessages = smessages, user = user)

#############################
## Getting Messages and files will used in ajax ##
## result is return via json ##
#############################
@dc.route('/<username>/get', methods = ['GET', 'POST'])
def get(username):
    user = User.query.filter_by(email = session['email']).first()
    rmessages = models.Message.query.filter_by(sender = username)
    return jsonify(rmessages) #we have to printecho with no html data besides this json data
    
#############################
## Sending Messages and files can be used in ajax ##
#############################
@dc.route('/<username>/send', methods = ['GET', 'POST'])
def send(username):
    user = User.query.filter_by(email = session['email']).first()
    rmessages = models.Message.query.filter_by(sender = username)
    smessages = models.Message.query.filter_by(receiver = username)
    message = MessageForm()

    PATH = "../dc/dc/static/uploads/%s/" % username

    poster = PostForm()
    user = User.query.filter_by(username = username).first()

    try:
        filename = secure_filename(poster.image.data.filename)
        poster.image.data.save(PATH+filename)
    except:
        filename = None

    try:
        if len(session['email']) > 0:
            visitor = User.query.filter_by(email = session['email']).first()
            post_ability = True
        else:
            visitor = None
            post_ability = False
    except KeyError:
        visitor = None
        post_ability = False

    if request.method == 'POST':
        if message.message.data == "" and message.message_image.data == "":
            post = models.Post(body = poster.content.data, timestamp = datetime.datetime.utcnow(), image= filename, author = user)
            temp_writer = models.Writer(username = visitor.username, firstname = visitor.firstname, lastname = visitor.lastname, email = visitor.email, image_location = visitor.image_location, cover_location = visitor.cover_location, who_wrote = post)
            db.session.add(post)
            db.session.add(temp_writer)
            db.session.commit()

            return render_template("p-profile.html", user = user, form = poster, message = message, post_ability = post_ability, pubs = pubdisplay_code, privs = privdisplay_code) 
        elif poster.content.data == "" and poster.image.data == "":
            try:
                message_filename = secure_filename(message.message_image.data.filename)
                message.message_image.data.save(PATH+filename)
            except:
                message_filename = None 
            mess = models.Message(sender = user.username, receiver = message.username.data,text = message.message.data, data_content = message_filename, date_sent = datetime.datetime.utcnow())
            db.session.add(mess)
            db.session.commit()
            response = {"message":message.message.data,"data_content":message_filename}
            #~ return render_template("send.html", message=json.dumps(response))
            return jsonify(response)
    elif request.method == 'GET':
        return render_template("p-profile.html", user = user, form = poster, message = message,  post_ability = post_ability)
        


##############
## Projects ##
##############

@dc.route('/<username>/projects')
def projects(username):
    user = User.query.filter_by(email = session['email']).first()

    if request.method == 'POST':
        pass
    return render_template('project.html', user = user)

@dc.route('/<username>/projects/new')
def new_project(username):
    user = User.query.filter_by(email = session['email']).first()
    return render_template('new_project.html', user = user)

#################################
## Networking and organization ##
#################################

@dc.route('/<username>/network')
def network(username):
    user = User.query.filter_by(email = session['email']).first()
    frnPub = models.publicFriend.query.filter_by(publicfriend = user)
    frnPriv = models.publicFriend.query.filter_by(publicfriend = user)
    return render_template('friends.html', publicfriends = frnPub, privatefriends = frnPriv, user =user)
