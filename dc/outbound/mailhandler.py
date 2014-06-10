import smtplib

MAIL_USERNAME  = 'dev.dreamscollective@gmail.com'
MAIL_PASSWORD  = '1Q2W3e4r_'   

def MakeContent():
	return "Thank you for signing up to Dreams Collective!"

def SendMail(r):
    msg = MakeContent()

    server = smtplib.SMTP('smtp.gmail.com:587')  
    server.starttls()  
    server.login(MAIL_USERNAME,MAIL_PASSWORD)  
    server.sendmail(MAIL_USERNAME, r, msg)  
    server.quit() 