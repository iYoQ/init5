from rest_framework import serializers
from rest_framework.settings import api_settings
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.db import IntegrityError, transaction
from .models import User
from .service import decode_uid


class AbstractUserSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    def get_email(self, obj):
        if obj.hide_email:
            return 'hidden'
        return obj.email
    
    class Meta:
        abstract = True

class UserSerializer(AbstractUserSerializer):
    ''' Show user profile
    '''
    post_count = serializers.IntegerField()
    comments_count = serializers.IntegerField()
    url = serializers.URLField(source='get_absolute_url')

    class Meta:
        model = User
        fields = ('email', 'username', 'url', 'rating', 'post_count', 'comments_count', 'date_registration', 'last_login', 'role', 'description', 'gender', 'birth_date', 'is_newsmaker')
        read_only_fields = ('username', 'role', 'is_newsmaker')


class UserListSerializer(AbstractUserSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'rating', 'last_login', 'role', 'description')


class AdminSerializer(serializers.ModelSerializer):
    '''Show user profile for admin
    '''
    post_count = serializers.IntegerField()
    comments_count = serializers.IntegerField()
    url = serializers.URLField(source='get_absolute_url')

    class Meta:
        model = User
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    default_error_messages = {
        'cannot_create_user': 'Unable to create account.'
    }


    class Meta:
        model = User
        fields = ('email', 'username', 'password')
    

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get('password')

        try:
            validate_password(password, user)
        except exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {'password': serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )
        
        return attrs
    
    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail('cannot_create_user')
        
        return user
    
    @transaction.atomic
    def perform_create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save(update_fields=['is_active'])
        return user


class UserActivationSerializer(serializers.Serializer):
    secret_code = serializers.CharField(write_only=True)

    default_error_messages = {
        'invalid_code': 'Invalid code.',
        'alredy_activate': 'Alredy activate.'
    }

    def validate(self, attrs):
        try:
            uid = decode_uid(attrs.get('secret_code', None))
            self.user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise ValidationError(
                {'error': [self.error_messages['invalid_code']]}, code='invalid_code'
            )
        if not self.user.is_active:
            return attrs

        raise ValidationError(
            {'error': [self.error_messages['alredy_activate']]}, code='alredy_activate'
        )


class UserRestorePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    default_error_messages = {
        'invalid_email': 'Email not found.',
        'alredy_activate': 'Alredy activate.'
    }

    def validate(self, attrs):
        try:
            user_email = attrs.get('email', None)
            self.user = User.objects.get(email=user_email)
            if self.user.is_active:
                return attrs
        except User.DoesNotExist:
            self.fail('invalid_email')


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('description', 'birth_date', 'gender', )


class AdminUpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('is_staff', 'description', 'is_newsmaker', 'role', 'is_active')
