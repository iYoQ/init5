from rest_framework import serializers
from ..articles.models import Category
from django.core.exceptions import ObjectDoesNotExist
from .service import change_or_add_users_changed_rating


class CommentOnlyParentListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class CommentRecursiveChildSerializer(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class CategoryRelatedField(serializers.RelatedField):
    default_error_messages = {
        'not_exist_category': 'Not exist category.'
    } 
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        try:
            category = Category.objects.get(name=data)
        except ObjectDoesNotExist:
            self.fail('not_exist_category')
        return category


class CurrentPasswordSerializer(serializers.Serializer):
    '''Request password for some changes
    '''

    current_password = serializers.CharField()

    default_error_messages = {
        'invalid_password': 'Invalid password'
    }

    def validate_current_password(self, value):
        is_password_valid = self.context['request'].user.check_password(value)
        if is_password_valid:
            return value
        self.fail('invalid_password')


class AdminDeleteSerializer(CurrentPasswordSerializer):
    '''Delete content
    '''
    pass

class ChangeRatingSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()

    default_error_messages = {
        'invalid_rating_value': 'Invalid rating value',
        'alredy_exists': 'Alredy exists'
    }


    class Meta:
        abstract = True

    def validate_rating(self, value):
        pos_value = -1
        neg_value = 1
        if value not in [pos_value, neg_value]:
            self.fail('invalid_rating_value')
        return value

    def update(self, instance, validated_data):
        change_or_add_users_changed_rating(self, instance, validated_data)

        instance = self.perform_update(instance)
        return instance

    def perform_update(self, instance):
        instance.save()
        return instance
