from config.celery import app
from .service import send
from .models import  MailingList


@app.task
def send_activation_email(user_email, secret_code):
    send(
        user_email,
        'Account activation',
        f'Your activation code: {secret_code}'
    )


@app.task
def send_new_password(user_email, password):
    send(
        user_email,
        'Your new password',
        f'Auto generated new password: {password}'
    )


@app.task
def send_selection():
    for user in MailingList.objects.all():
        send(
            user.email,
            'Thanks for subscribed',
            'expect a lot of spam'
        )