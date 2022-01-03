from django.db import models
from users.models import User
    

class Post(models.Model):
    headline = models.CharField(max_length=200)
    content = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    number_of_comments = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    is_article = models.BooleanField()
    is_news = models.BooleanField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.headline}'
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ('date_create', )


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ('date_create', )
    
    def __str__(self):
        return f'Comment by {self.user} on {self.post}.'
