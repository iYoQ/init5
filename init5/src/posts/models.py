from django.db import models
from django.conf import settings

RATING_CHOOSE = (
    ('1', 1),
    ('2', 2),
    ('3', 3),
    ('4', 4),
    ('5', 5),
)


class Post(models.Model):
    headline = models.CharField(max_length=200)
    content = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    number_of_comments = models.IntegerField(default=0)
    rating = models.FloatField(choices=RATING_CHOOSE, default=0)
    users_changed_rating = models.JSONField(default=dict, null=True)
    is_article = models.BooleanField()
    is_news = models.BooleanField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_author')


    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ('date_create', )


    def __str__(self):
        return f'{self.headline}'

    def count_users_changed_rating(self):
        count_users = len(self.users_changed_rating.keys())
        return count_users
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_author')
    content = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    rating = models.FloatField(choices=RATING_CHOOSE, default=0)
    users_changed_rating = models.JSONField(default=dict, null=True)


    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ('date_create', )


    def __str__(self):
        return f'Comment by {self.user} on {self.post}.'
