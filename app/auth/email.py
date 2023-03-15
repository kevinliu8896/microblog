from flask import render_template, current_app
from flask_babel import _
from app.email import send_email
from email.message import EmailMessage
import ssl
import smtplib

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(_('[Microblog] Reset Your Password'),
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))

def send_verification_code(user, code):
    email_sender = 'compo4110microblog@gmail.com'
    email_password = 'vvtmpclzsppytvyx'
    email_receiver = user.email

    subject = 'Verification Email'
    body = "Your verification code is: " + str(code)

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

