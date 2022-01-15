from rest_framework import serializers
from .service import check_or_add_users_changed_rating
from .models import News
from ..comments.serializers import NewsListCommentSeriazlier

class NewsListSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    number_of_users_changed_rating = serializers.IntegerField(source='count_users_changed_rating')
    comments_count = serializers.IntegerField(source='get_comments_count', read_only=True)

    class Meta:
        model = News
        fields = ('id', 'headline', 'content', 'date_update','number_of_users_changed_rating', 'view_count', 'comments_count', 'rating', 'author')


class NewsSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    number_of_users_changed_rating = serializers.IntegerField(source='count_users_changed_rating')
    comments_count = serializers.IntegerField(source='get_comments_count', read_only=True)
    comments = NewsListCommentSeriazlier(many=True, read_only=True)

    class Meta:
        model = News
        fields = ('id', 'headline', 'content', 'date_update', 'view_count', 'comments_count', 'comments', 'number_of_users_changed_rating', 'users_changed_rating', 'rating', 'author', )


class NewsCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ('headline', 'content', )


class NewsChangeRatingSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField()

    default_error_messages = {
        'invalid_rating_value': 'Invalid rating value',
        'alredy_exists': 'Alredy exists'
    }

    class Meta:
        model = News
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

        instance = self.perform_update(instance)
        return instance

    def perform_update(self, instance):
        instance.rating = round(instance.rating, 1)
        instance.save()
        return instance


class AdminListSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    number_of_users_changed_rating = serializers.IntegerField(source='count_users_changed_rating')
    comments_count = serializers.IntegerField(source='get_comments_count', read_only=True)
    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = News
        fields = ('__all__')


class AdminDetailSerializer(AdminListSerializer):
    comments = NewsListCommentSeriazlier(many=True, read_only=True)

    class Meta:
        model = News
        fields = ('__all__')