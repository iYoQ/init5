from config.celery import app
from .service import send

@app.task
def send_activation_email(user_email, secret_code):
    send(user_email, secret_code)