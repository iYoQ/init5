from config.celery import app
from .service import send

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