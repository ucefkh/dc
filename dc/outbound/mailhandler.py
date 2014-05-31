import smtplib

recipients = []
cause = []

def MakeContent():
	return """

	<!DOCTYPE html>
	<html>
		<head>
		<title>Welcome!</title>
		</head>
		<body>
			<h>Thanks for signing up!</h>
		</body>
		</html>

	"""

# Synthesis? Hmm. Backlogged.

def SendMail():
     
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
     
    sender = 'dev.dreamscollective@gmail.com'
    recipient = 'mail@arsalanbashir.com'
    subject = 'Gmail SMTP Test'
    body = MakeContent()
     
    """Sends an e-mail to the specified recipient."""
     
    body = "" + body + ""
     
    headers = ["From: " + sender,
               "Subject: " + subject,
               "To: " + recipient,
               "MIME-Version: 1.0",
               "Content-Type: text/html"]
    headers = "\r\n".join(headers)
     
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
     
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(sender, "1Q2W3e4r_")
     
    session.sendmail(sender, recipient, headers + "\r\n\r\n" + body)
    session.quit()
	
	# return render_template('contact.html')