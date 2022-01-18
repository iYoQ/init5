from django.db import models
from django.conf import settings
from django.urls import reverse


class News(models.Model):

    headline = models.CharField(max_length=200)
    content = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='news')


    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'
        ordering = ('date_create', )


    def __str__(self):
        return f'{self.headline}'
    
    def get_comments_count(self):
        return self.comments.count()
    
    def get_absolute_url(self):
        return reverse('news-detail', kwargs={'pk': self.pk})
