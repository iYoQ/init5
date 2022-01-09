from django.db.utils import IntegrityError
from rest_framework import serializers
from .service import check_or_add_users_changed_rating
from .models import (
    Post,
    Comment
)


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username')
    id = serializers.IntegerField(read_only=True)
    number_of_users_changed_rating = serializers.IntegerField(source='count_users_changed_rating')

    class Meta:
        model = Post
        fields = ('id', 'headline', 'content', 'date_update', 'number_of_users_changed_rating', 'number_of_comments', 'users_changed_rating', 'rating', 'author', )
    

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
        user = self.context['request'].user
        new_user_rating = validated_data.get('rating', instance.rating)
        coefficient = 0.1
        
        check_or_add_users_changed_rating(self, instance, user, new_user_rating, coefficient)

        rating_coefficient = new_user_rating*coefficient
        instance.rating += rating_coefficient
        instance.rating = round(instance.rating, 1)
        instance.save()
        return instance


class NewsSerializer(ArticleSerializer):
    pass
