from rest_framework import serializers
from .service import check_or_add_users_changed_rating
from .models import (
    Article,
    News,
    ArticleComment,
    NewsComment
)
from ..general.serializers import (
    CommentRecursiveChildSerializer,
    CommentOnlyParentListSerializer
)


########################################
# Comments Serializers
########################################

class AbstractCreateCommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        abstract = True


class AbstractListCommentSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()
    children = CommentRecursiveChildSerializer(many=True)

    def get_content(self, obj):
        if obj.deleted:
            return None
        return obj.content
    
    class Meta:
        abstract = True


class CreateArticleCommentSerializer(AbstractCreateCommentSerializer):

    class Meta:
        model = ArticleComment
        fields = ('id', 'article', 'content', 'parent')


class CreateNewsCommentSerializer(AbstractCreateCommentSerializer):

    class Meta:
        model = NewsComment
        fields = ('id', 'news', 'content', 'parent')


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


########################################
# Change Rating Serializers
########################################

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


########################################
# Abstract Articles and News Seriazlier
########################################

class AbstractPostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    number_of_users_changed_rating = serializers.IntegerField(source='count_users_changed_rating')

    class Meta:
        abstract = True


########################################
# Article Serializers
########################################

class ArticleSerializer(AbstractPostSerializer):
    comments = ArticleListCommentSeriazlier(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'headline', 'content', 'date_update', 'view_count', 'comments_count', 'comments',  'number_of_users_changed_rating', 'users_changed_rating', 'rating', 'author', )


class ArticleCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('headline', 'content', )


class ArticleChangeRatingSerializer(ChangeRatingSerializer):

    class Meta:
        model = Article
        fields = ('rating', )


########################################
# News Seriazliers
########################################

class NewsSerializer(AbstractPostSerializer):
    comments = NewsListCommentSeriazlier(many=True, read_only=True)

    class Meta:
        model = News
        fields = ('id', 'headline', 'content', 'date_update', 'view_count', 'comments_count', 'comments', 'number_of_users_changed_rating', 'users_changed_rating', 'rating', 'author', )


class NewsCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ('headline', 'content', )


class NewsChangeRatingSerializer(ChangeRatingSerializer):

    class Meta:
        model = News
        fields = ('rating', )
