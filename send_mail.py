from smtplib import SMTP
import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(subject, text):
    try:
        server = SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(config.EMAIL, config.PASSWORD)
        t = MIMEText(text, 'plain')
        t['Subject'] = subject
        server.sendmail(config.EMAIL, config.EMAIL, t.as_string())
        server.quit()
    except:
        print('Email failed.')
