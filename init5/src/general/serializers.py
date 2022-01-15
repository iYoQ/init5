from rest_framework import serializers
from ..articles.models import Category
from django.core.exceptions import ObjectDoesNotExist


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
