from django.db import models
from users.models import User
from django.contrib.postgres.fields import ArrayField

RATING_VALUE = [
    ('1', 1),
    ('2', 2),
    ('3', 3),
    ('4', 4),
    ('5', 5),
]


class Post(models.Model):
    headline = models.CharField(max_length=200)
    content = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    number_of_comments = models.IntegerField(default=0)
    rating = models.FloatField(choices=RATING_VALUE ,default=0)
    users_changed_rating = models.JSONField(null=True)
    is_article = models.BooleanField()
    is_news = models.BooleanField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ('date_create', )


    def __str__(self):
        return f'{self.headline}'

    def save(self, *args, **kwargs):
        self.rating = round(self.rating, 1)
        super().save(*args, **kwargs)
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    rating = models.FloatField(choices=RATING_VALUE ,default=0)
    users_changed_rating = models.JSONField(null=True)


    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ('date_create', )


    def __str__(self):
        return f'Comment by {self.user} on {self.post}.'
    
    def save(self, *args, **kwargs):
        self.rating = round(self.rating, 1)
        super().save(*args, **kwargs)
