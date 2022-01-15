from rest_framework import serializers


class CommentOnlyParentListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class CommentRecursiveChildSerializer(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


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
