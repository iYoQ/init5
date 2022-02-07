import datetime
from config.celery import app
from django.conf import settings
from django.db.models import Q
from .models import MailingList
from ..articles.models import Article
from ..articles.serializers import ArticleListSerializer
from .service import send


@app.task
def send_confirmation_email(user_email, encode_uid, token):
    send(
        user_email,
        'Account activation',

        f'Follow link: {settings.SITE_LINK}/activate/{encode_uid}/{token}'
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
    articles = Article.objects.filter(date_create__gte=datetime.date.today()-datetime.timedelta(days=7)).order_by('-rating')[:10]
    articles_list = []
    for article in articles:
        articles_list.append(article.headline)
    for user in MailingList.objects.all():
        send(
            user.email,
            'Thanks for subscribed',
            f'Top:\n {articles_list}'
            )
