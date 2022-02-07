import datetime
from config.celery import app
from django.conf import settings
from django.template import loader
from .models import MailingList
from ..articles.models import Article
from .service import send


@app.task
def send_activation_email(user_email, encode_uid, token):
    html_message = loader.render_to_string(
        'activation.html',
        {
            'url': f'{settings.SITE_LINK}/activate/{encode_uid}/{token}'
        }
    )
    send(
        user_email,
        'Account activation',
        html_message
    )


@app.task
def send_change_password_confirmation(user_email, encode_uid, token):
    html_message = loader.render_to_string(
        'change_password.html',
        {
            'url': f'{settings.SITE_LINK}/change-password/{encode_uid}/{token}'
        }
    )
    send(
        user_email,
        'Restore password',
        html_message
    )


@app.task
def send_new_password(user_email, password):
    html_message = loader.render_to_string(
        'new_password.html',
        {
            'url': password
        }
    )
    send(
        user_email,
        'Your new password',
        html_message
    )


@app.task
def send_selection():
    articles = Article.objects.filter(date_create__gte=datetime.date.today()-datetime.timedelta(days=7)).order_by('-rating')[:10]

    html_message = loader.render_to_string(
        'articles_selection.html',
        {
            'articles': articles
        }
    )

    for user in MailingList.objects.all():
        send(
            user.email,
            'Thanks for subscribed',
            html_message=html_message
        )
