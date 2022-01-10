from django.db import models
from django.conf import settings


class AbstractPost(models.Model):
    headline = models.CharField(max_length=200)
    content = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0)
    rating = models.FloatField(choices=settings.RATING_CHOOSE, default=0)
    users_changed_rating = models.JSONField(default=dict, null=True)
    active = models.BooleanField(default=True)
    moderation = models.BooleanField(default=False)


    class Meta:
        abstract = True


    def __str__(self):
        return f'{self.headline}'

    def count_users_changed_rating(self):
        count_users = len(self.users_changed_rating.keys())
        return count_users
    
    def comments_count(self):
        return self.comments.count()


class AbstractComment(models.Model):
    content = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    rating = models.FloatField(choices=settings.RATING_CHOOSE, default=0)
    users_changed_rating = models.JSONField(default=dict, null=True)


    class Meta:
        abstract = True
