import smtplib
import authorization

def MakeContent(template):
	return """

	<!DOCTYPE html>
	<html>
		<head>
		<title>Welcome!</title>
		</head>
		<body>
			<h>Thanks for signing up! This is the %s template.</h>
		</body>
		</html>

		""" % template

# Synthesis? Hmm. Backlogged.

def SendMail(template, recipients):     
    body = MakeContent(template)
    subject = "Title"
    """Sends an e-mail to the specified recipient."""
     
    body = "" + body + ""
     
    headers = ["From: " + MAIL_USERNAME,
               "Subject: " + subject,
               "To: " + recipient,
               "MIME-Version: 1.0",
               "Content-Type: text/html"]
    headers = "\r\n".join(headers)
     
    session = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
     
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(MAIL_USERNAME, MAIL_PASSWORD)
     
    session.sendmail(MAIL_USERNAME, recipient, headers + "\r\n\r\n" + body)
    session.quit()
	
	# return render_template('contact.html')