import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from backend.settings import *
from smtplib import SMTPResponseException





def send_mail(html_content, subject, to_email ):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = EMAIL_HOST_USER
    msg['To'] = to_email

    msg.attach(MIMEText(html_content, 'html'))

    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.sendmail(EMAIL_HOST_USER, to_email, msg.as_string())
        server.quit()
    except SMTPResponseException as e:
        print("error")