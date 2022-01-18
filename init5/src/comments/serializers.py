from django.conf import settings
from rest_framework import serializers
from .models import (
    ArticleComment,
    NewsComment
)
from ..general.serializers import (
    CommentRecursiveChildSerializer,
    CommentOnlyParentListSerializer,
    ChangeRatingSerializer
)


class AbstractCommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        abstract = True


class AbstractListCommentSerializer(AbstractCommentSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    children = CommentRecursiveChildSerializer(many=True)
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        if obj.deleted:
            return None
        return obj.content
    
    class Meta:
        abstract = True


class ArticleCommentSerializer(AbstractCommentSerializer):
    default_error_messages = {
        'cannot_create_comment': 'Cannot create comment, wrong data.'
    }


    class Meta:
        model = ArticleComment
        fields = ('id', 'post', 'author', 'content', 'rating', 'deleted', 'parent')
    
    def create(self, validated_data):
        if not validated_data.get('parent') or validated_data['parent'].post == validated_data['post']:
            return self.Meta.model.objects.create(**validated_data)
        return self.fail('cannot_create_comment')


class NewsCommentSerializer(AbstractCommentSerializer):

    class Meta:
        model = NewsComment
        fields = ('id', 'post', 'author', 'rating', 'content', 'deleted', 'parent')
    
    def create(self, validated_data):
        if not validated_data.get('parent') or validated_data['parent'].post == validated_data['post']:
            return self.Meta.model.objects.create(**validated_data)
        return self.fail('cannot_create_comment')


class ArticleListCommentSeriazlier(AbstractListCommentSerializer):

    class Meta:
        list_serializer_class = CommentOnlyParentListSerializer
        model = ArticleComment
        fields = ('id', 'post', 'author', 'content', 'rating', 'date_create', 'date_update', 'deleted', 'children')


class NewsListCommentSeriazlier(AbstractListCommentSerializer):

    class Meta:
        list_serializer_class = CommentOnlyParentListSerializer
        model = NewsComment
        fields = ('id', 'post', 'author', 'content', 'rating', 'date_create', 'date_update', 'deleted', 'children')


class ArticleCommentChangeRatingSerializer(ChangeRatingSerializer):

    class Meta:
        model = ArticleComment
        fields = ('rating', )


class NewsCommentChangeRatingSerializer(ChangeRatingSerializer):

    class Meta:
        model = NewsComment
        fields = ('rating', )


class UserCommentsSerializer(serializers.Serializer):
    author = serializers.CharField(source='author.username', read_only=True)
    content = serializers.CharField()
    rating = serializers.IntegerField()
    date_create = serializers.DateTimeField()
    post_url = serializers.URLField(source='get_post_url')
