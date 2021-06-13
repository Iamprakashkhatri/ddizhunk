from celery.decorators import task
from django.contrib.auth.models import User
from django.core.mail import send_mail

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


@task(name="send_mail_notification")
def send_email(subject, message, html_content, to_mail):
    send_mail(
        subject=subject, message=message, html_message=html_content, recipient_list=to_mail,
        from_email='noreply@padhaisewa.com', fail_silently=True
    )

# @background(schedule=1)
def send_subscription_email(subscribers, newsletter):
    content = newsletter['contents']
    subject = newsletter['subject']
    for subscriber in subscribers:
        email = subscriber['email']
        code = subscriber['conf_code']
        html_content = content + f'<br><a href=http://127.0.0.1:8000/api/accounts/unsubscribe/?email={email}&conf_code={code}>unsubscribe</a>'
        send_mail(subject=subject, message=None, from_email='testing100quantum@gmail.com', recipient_list=[email, ],
                  html_message=html_content)

