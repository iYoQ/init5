from django.db.models import fields
from django.db.utils import IntegrityError
from rest_framework import serializers
from django.core import exceptions

from .models import *


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username')
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'headline', 'content', 'date_update', 'number_of_comments', 'rating', 'author', )
    


class ArticleCreateSerializer(serializers.ModelSerializer):

    default_error_messages = {
        'cannot_create_article': 'Unable to create article.'
    }

    class Meta:
        model = Post
        fields = ('headline', 'content', )
    

    def create(self, validated_data):
        is_article = True
        is_news = False
        user = self.context['request'].user
        try:    
            article = Post.objects.create(author=user, is_article=is_article, is_news=is_news, **validated_data)
        except IntegrityError:
            self.fail('cannot_create_article')

        return article


class NewsCreateSerializer(serializers.ModelSerializer):

    default_error_messages = {
        'cannot_create_news': 'Unable to create news.'
    }

    class Meta:
        model = Post
        fields = ('headline', 'content', )
    

    def create(self, validated_data):
        is_article = False
        is_news = True
        user = self.context['request'].user
        try:    
            news = Post.objects.create(author=user, is_article=is_article, is_news=is_news, **validated_data)
        except IntegrityError:
            self.fail('cannot_create_news')

        return news


class UpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('headline', 'content', )


class NewsSerializer(ArticleSerializer):
    pass
