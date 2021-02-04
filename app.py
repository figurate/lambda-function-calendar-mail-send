import email.utils
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

DEFAULT_HOST = "host.docker.internal"
DEFAULT_PORT = 1025

if "HOST" not in os.environ:
    print("SMTP host not configured")
    HOST = DEFAULT_HOST
else:
    HOST = os.environ["HOST"]

if "PORT" not in os.environ:
    print("SMTP host not configured")
    PORT = DEFAULT_PORT
else:
    PORT = os.environ["PORT"]

if "USERNAME_SMTP" not in os.environ:
    print("SMTP user not configured")
    USERNAME_SMTP = "user"
else:
    USERNAME_SMTP = os.environ["USERNAME_SMTP"]

if "PASSWORD_SMTP" not in os.environ:
    print("SMTP password not configured")
    PASSWORD_SMTP = "pass"
else:
    PASSWORD_SMTP = os.environ["PASSWORD_SMTP"]

TLS_ENABLED = False
AUTH_ENABLED = False

def handler(event, context):
    print(f'Received event: {event}')

    message = MIMEMultipart('alternative')
    message['Subject'] = event['subject']
    message['From'] = email.utils.formataddr((event['organizerName'], event['organizer']))
    message['To'] = ",".join(event['attendees'])

    part1 = MIMEText(event['bodyText'], 'plain')
    part2 = MIMEText(event['bodyHTML'], 'html')
    part3 = MIMEText(event['calendar'], f'calendar;method={event["method"]}', 'UTF-8')

    message.attach(part1)
    message.attach(part2)
    message.attach(part3)

    send_mail(event['organizer'], ",".join(event['attendees']), message.as_string())


def send_mail(sender, recipients, message):
    try:
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        if TLS_ENABLED:
            server.starttls()
            server.ehlo()
        if AUTH_ENABLED:
            server.login(USERNAME_SMTP, PASSWORD_SMTP)
        server.sendmail(sender, recipients, message)
    except Exception as e:
        print("Error: ", e)
    else:
        print("Email sent!")
