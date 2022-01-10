from __future__ import annotations
from django.db.utils import IntegrityError
from rest_framework import serializers
from .service import check_or_add_users_changed_rating
from .models import (
    Article,
    News,
    ArticleComment,
    NewsComment
)
from src.general.serializers import (
    CommentRecursiveChildSerializer,
    CommentOnlyParentListSerializer
)


class CreateArticleCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleComment
        fields = ('article', 'content', 'parent')


class CreateNewsCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsComment
        fields = ('news', 'content', 'parent')


class AbstractListCommentSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()
    children = CommentRecursiveChildSerializer(many=True)

    def get_content(self, obj):
        if obj.deleted:
            return None
        return obj.content
    
    class Meta:
        abstract = True


class ArticleListCommentSeriazlier(AbstractListCommentSerializer):

    class Meta:
        list_serializer_class = CommentOnlyParentListSerializer
        model = ArticleComment
        fields = ('id', 'article', 'content', 'date_create', 'date_update', 'deleted', 'children')


class NewsListCommentSeriazlier(AbstractListCommentSerializer):

    class Meta:
        list_serializer_class = CommentOnlyParentListSerializer
        model = NewsComment
        fields = ('id', 'news', 'content', 'date_create', 'date_update', 'deleted', 'children')


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    number_of_users_changed_rating = serializers.IntegerField(source='count_users_changed_rating')
    comments = ArticleListCommentSeriazlier(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'headline', 'content', 'date_update', 'view_count', 'comments_count', 'comments',  'number_of_users_changed_rating', 'users_changed_rating', 'rating', 'author', )


class NewsSerializer(ArticleSerializer):
    
    author = serializers.CharField(source='author.username', read_only=True)
    number_of_users_changed_rating = serializers.IntegerField(source='count_users_changed_rating')
    comments = NewsListCommentSeriazlier(many=True, read_only=True)

    class Meta:
        model = News
        fields = ('id', 'headline', 'content', 'date_update', 'view_count', 'comments_count', 'comments', 'number_of_users_changed_rating', 'users_changed_rating', 'rating', 'author', )


class ArticleCreateSerializer(serializers.ModelSerializer):

    default_error_messages = {
        'cannot_create_article': 'Unable to create article.'
    }

    class Meta:
        model = Article
        fields = ('headline', 'content', )
    

    def create(self, validated_data):
        user = self.context['request'].user
        try:    
            article = Article.objects.create(author=user, **validated_data)
        except IntegrityError:
            self.fail('cannot_create_article')

        return article


class NewsCreateSerializer(serializers.ModelSerializer):

    default_error_messages = {
        'cannot_create_news': 'Unable to create news.'
    }

    class Meta:
        model = News
        fields = ('headline', 'content', )
    

    def create(self, validated_data):
        user = self.context['request'].user
        try:    
            news = News.objects.create(author=user, **validated_data)
        except IntegrityError:
            self.fail('cannot_create_news')

        return news


class ArticleUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('headline', 'content', )


class NewsUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ('headline', 'content', )


class ChangeRatingSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField()

    default_error_messages = {
        'invalid_rating_value': 'Invalid rating value',
        'alredy_exists': 'Alredy exists'
    }

    class Meta:
        abstract = True


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

        instance = self.perform_update(instance)
        return instance

    def perform_update(self, instance):
        instance.rating = round(instance.rating, 1)
        instance.save()
        return instance


class ArticleChangeRatingSerializer(ChangeRatingSerializer):
    class Meta:
        model = Article
        fields = ('rating', )


class NewsChangeRatingSerializer(ChangeRatingSerializer):
    class Meta:
        model = News
        fields = ('rating', )


