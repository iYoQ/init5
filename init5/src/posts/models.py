from django.db import models
from django.conf import settings
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

from .abstract_models import AbstractComment, AbstractPost


class Article(AbstractPost):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')


    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ('date_create', )


class News(AbstractPost):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='news')


    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'
        ordering = ('date_create', )


class NewsComment(AbstractComment, MPTTModel):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')


    def __str__(self):
        return f'Comment by {self.author} in {self.news}.'


class ArticleComment(AbstractComment, MPTTModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')


    def __str__(self):
        return f'Comment by {self.author} in {self.article}.'
