import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from platform import python_version


def send_mail(mail: str, number: int):
    server = 'smtp.mail.ru'
    user = 'tozlovanu.sandu@mail.ru'
    password = 'augiqkmjXVNnijWTYa07'

    recipients = [mail]
    sender = 'tozlovanu.sandu@mail.ru'
    subject = 'Portfolio Confirmation Code'
    text = f"Confirmation code: {number}"
    html = '<html><head></head><body><p>' + text + '</p></body></html>'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = 'Python script <' + sender + '>'
    msg['To'] = ', '.join(recipients)
    msg['Reply-To'] = sender
    msg['Return-Path'] = sender
    msg['X-Mailer'] = 'Python/' + (python_version())

    part_text = MIMEText(text, 'plain')
    part_html = MIMEText(html, 'html')

    msg.attach(part_text)
    msg.attach(part_html)

    mail = smtplib.SMTP_SSL(server)
    mail.login(user, password)
    mail.sendmail(sender, recipients, msg.as_string())
    mail.quit()
