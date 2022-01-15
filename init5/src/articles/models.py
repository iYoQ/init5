from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class Article(models.Model):
    headline = models.CharField(max_length=200)
    content = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0)
    rating = models.IntegerField(default=0)
    users_changed_rating = models.JSONField(default=dict, null=True, blank=True)
    active = models.BooleanField(default=True)
    moderation = models.BooleanField(default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles')


    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ('date_create', )


    def __str__(self):
        return f'{self.headline}'

    def count_users_changed_rating(self):
        count_users = len(self.users_changed_rating.keys())
        return count_users
    
    def get_comments_count(self):
        return self.comments.count()

