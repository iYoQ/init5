from rest_framework import serializers
from .models import (
    Article,
    Category,
)
from ..general.serializers import CategoryRelatedField, ChangeRatingSerializer
from ..comments.serializers import ArticleListCommentSerializer


class ArticleListSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    number_of_users_changed_rating = serializers.IntegerField(source='count_users_changed_rating')
    comments_count = serializers.IntegerField(source='get_comments_count', read_only=True)
    category = serializers.CharField(source='category.name', read_only=True)
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        if len(obj.content) > 1000:
            return obj.content[:1000] + '...'
        return obj.content

    class Meta:
        model = Article
        fields = ('id', 'headline', 'category', 'content', 'date_create', 'date_update', 'view_count', 'comments_count', 'rating', 'number_of_users_changed_rating', 'author')


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    number_of_users_changed_rating = serializers.IntegerField(source='count_users_changed_rating')
    comments_count = serializers.IntegerField(source='get_comments_count', read_only=True)
    comments = ArticleListCommentSerializer(many=True, read_only=True)
    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'headline', 'content', 'category', 'date_create', 'date_update', 'view_count', 'comments_count', 'comments',  'number_of_users_changed_rating', 'rating', 'author', )


class ArticleCreateUpdateSerializer(serializers.ModelSerializer):
    category = CategoryRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Article
        fields = ('headline', 'category', 'content', 'date_create', 'date_update', )


class ArticleChangeRatingSerializer(ChangeRatingSerializer):

    class Meta:
        model = Article
        fields = ('rating', )


class AdminListSerializer(ArticleListSerializer):

    class Meta:
        model = Article
        fields = ('__all__')


class AdminDetailSerializer(ArticleSerializer):
    comments = ArticleListCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ('__all__')


class AdminUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('headline', 'content', 'active', 'moderation', 'category', 'date_create', 'date_update', )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', )