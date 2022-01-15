from rest_framework import serializers
from .models import (
    ArticleComment,
    NewsComment
)
from ..general.serializers import (
    CommentRecursiveChildSerializer,
    CommentOnlyParentListSerializer,
)


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
