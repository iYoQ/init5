from django.contrib import admin
from .models import *


class PostsAdmin(admin.ModelAdmin):
    list_display = ('headline',
    'content',
    'date_create',
    'date_update',
    'number_of_comments',
    'rating',
    'is_article',
    'is_news',
    'author',)
    list_filter = ('date_create', )
    search_fields = ('headline', )

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('post',
    'author',
    'content',
    'date_create',
    'date_update',
    'active',
    'rating',)
    list_filter = ('date_create', )
    search_fields = ('user', )

# admin.site.register(Comment, CommentsAdmin)
# admin.site.register(Post, PostsAdmin)
