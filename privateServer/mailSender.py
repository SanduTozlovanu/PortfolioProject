import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from platform import python_version

from publicServer.config.definitions import EMAIL, EMAIL_PASSWORD, SMTP_SERVER


def send_mail(mail: str, number: int):
    server = SMTP_SERVER
    user = EMAIL
    password = EMAIL_PASSWORD

    recipients = [mail]
    sender = EMAIL
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
