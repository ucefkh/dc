from flask.ext.mail import Message, Mail

dc.config['MAIL_SERVER']='smtp.gmail.com'
dc.config['MAIL_PORT'] = 465
dc.config['MAIL_USERNAME'] = 'dev.dreamscollective@gmail.com'
dc.config['MAIL_PASSWORD'] = 'xx;'		# 	You wish, loser!
dc.config['MAIL_USE_TLS'] = False
dc.config['MAIL_USE_SSL'] = True

mail.init_app(dc)