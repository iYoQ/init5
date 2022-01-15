from rest_framework import serializers
from rest_framework.settings import api_settings
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.db import IntegrityError, transaction
from .models import User
from ..general.serializers import CurrentPasswordSerializer


class UserSerializer(serializers.ModelSerializer):
    ''' Show user profile
    '''


    class Meta:
        model = User
        fields = ('email', 'username', 'url', 'date_registration', 'last_login', 'role', 'description', 'gender', 'birth_date', 'is_newsmaker')
        read_only_fields = ('username', 'role', 'is_newsmaker')


class AdminSerializer(serializers.ModelSerializer):
    '''Show user profile for admin
    '''


    class Meta:
        model = User
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
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
        return user


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'description', 'birth_date', 'gender', )


class AdminUpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('is_staff', 'is_active', 'description', 'is_newsmaker', 'role')


class AdminDeleteSerializer(CurrentPasswordSerializer):
    '''Delete content
    '''
    pass