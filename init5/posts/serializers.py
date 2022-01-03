from django.db.models import fields
from django.db.utils import IntegrityError
from rest_framework import serializers
from django.core import exceptions
import json
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


class ChangeRatingSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField()

    default_error_messages = {
        'invalid_rating_value': 'Invalid rating value',
        'alredy_exists': 'Alredy exists'
    }

    class Meta:
        model = Post
        fields = ('rating', )


    def validate_rating(self, value):
        min_value = 0
        max_value = 5
        if value <= min_value or value > max_value:
            self.fail('invalid_rating_value')
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user.username
        user_rating = validated_data.get('rating', instance.rating)
        coefficient = 0.1

        if instance.users_changed_rating.get(user):
            return self.fail('alredy_exists')

        instance.users_changed_rating[user] = user_rating
        
        rating_coefficient = user_rating*coefficient
        instance.rating += rating_coefficient
        instance.save()
        return instance


class NewsSerializer(ArticleSerializer):
    pass
