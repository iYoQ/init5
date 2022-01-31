from rest_framework import serializers
from .models import News
from ..comments.serializers import NewsListCommentSerializer


class NewsListSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    comments_count = serializers.IntegerField(source='get_comments_count', read_only=True)
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        if len(obj.content) > 1000:
            return obj.content[:1000] + '...'
        return obj.content

    class Meta:
        model = News
        fields = ('id', 'headline', 'content', 'date_update', 'view_count', 'comments_count', 'author')


class NewsSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    comments_count = serializers.IntegerField(source='get_comments_count', read_only=True)
    comments = NewsListCommentSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = ('id', 'headline', 'content', 'date_update', 'view_count', 'comments_count', 'comments', 'author', )


class NewsCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ('headline', 'content', 'date_update', )


class AdminListSerializer(NewsListSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    comments_count = serializers.IntegerField(source='get_comments_count', read_only=True)

    class Meta:
        model = News
        fields = ('__all__')


class AdminDetailSerializer(NewsSerializer):
    comments = NewsListCommentSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = ('__all__')


class AdminUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ('headline', 'content', 'active', 'date_update', )