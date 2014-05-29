"""
send scripts

use mailchimp API 

receive and send auto responses

"""

recipients = []
cause = []

def MakeContent(template, cause):
	pass

# Synthesis? Hmm. Backlogged.

def SendMail(content, recipients):
	msg = Message(form.subject.data, sender='dev.dreamscollective@gmail.com', recipients=recipients)
	msg.body = MakeContent(template, cause)
	mail.send(msg)
	
	# return render_template('contact.html')