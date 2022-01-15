from django.db import models
from django.conf import settings


class News(models.Model):
    RATING_CHOOSE = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)

    headline = models.CharField(max_length=200)
    content = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0)
    rating = models.FloatField(choices=RATING_CHOOSE, default=0)
    users_changed_rating = models.JSONField(default=dict, null=True, blank=True)
    active = models.BooleanField(default=True)
    moderation = models.BooleanField(default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='news')


    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'
        ordering = ('date_create', )


    def __str__(self):
        return f'{self.headline}'

    def count_users_changed_rating(self):
        count_users = len(self.users_changed_rating.keys())
        return count_users
    
    def get_comments_count(self):
        return self.comments.count()
