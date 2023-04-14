#!/usr/bin/python3

#http://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python
#In the above link, look for Anthony Hilyard's answer and check the more comments
# because there has been a lot of changes in terms of authentication.
# This situation is also well summarized at the following
#http://stackabuse.com/how-to-send-emails-with-gmail-using-python/
#http://naelshiab.com/tutorial-send-email-python/
import smtplib

def send_email(user, pwd, recipient, subject, body):
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        return 0
    except:
        return 1
#    print 'successfully sent the mail'

def sendmail(recipient, subject, body):
    return send_email('yb174atsk@gmail.com', 'TfjLQ335', recipient, subject, body)
    
if __name__ == "__main__":        
    send_email('yb174atsk@gmail.com', 'TfjLQ335', 'thkimatmit@gmail.com', 'Test', 'Python e-mail testing')
