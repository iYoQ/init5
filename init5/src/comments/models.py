from django.db import models
from django.conf import settings
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from ..articles.models import Article
from ..news.models import News


class AbstractComment(models.Model):
    content = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    rating = models.FloatField(default=0)
    users_changed_rating = models.JSONField(default=dict, null=True)


    class Meta:
        abstract = True


class ArticleComment(AbstractComment, MPTTModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')


    class MPTTMeta:
        order_insertion_by = ['-date_create']

    def __str__(self):
        return f'Comment by {self.author} in {self.article}.'


class NewsComment(AbstractComment, MPTTModel):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')


    class MPTTMeta:
        order_insertion_by = ['-date_create']

    def __str__(self):
        return f'Comment by {self.author} in {self.news}.'
