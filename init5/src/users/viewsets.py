from xml.dom import ValidationErr
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth import logout
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from .models import User
from rest_framework.mixins import (
    RetrieveModelMixin, 
    UpdateModelMixin, 
    DestroyModelMixin, 
    ListModelMixin
)
from rest_framework.permissions import (
    AllowAny, 
    IsAdminUser, 
    IsAuthenticated, 
    IsAuthenticatedOrReadOnly
)
from ..articles.serializers import ArticleListSerializer
from ..general.permissions import UserIsOwnerOrAdmin
from ..general.serializers import AdminDeleteSerializer
from ..general.paginations import UserPagination
from .tasks import send_activation_email, send_new_password
from .service import encode_uid
from .serializers import *


class UserViewSet(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    pagination_class = UserPagination
    filter_backends = [filters.SearchFilter]
    permission_classes = [AllowAny]
    search_fields = ['username']
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'head', 'patch', 'options', 'delete']

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = User.objects.all()
        else:
            queryset = User.objects.filter(is_active=True)
        return queryset

    def get_permissions(self):
        if self.action == 'partial_update':
            self.permission_classes = [IsAdminUser]
        elif self.action == 'destroy':
            self.permission_classes = [IsAdminUser]
        elif self.action == 'me':
            self.permission_classes = [UserIsOwnerOrAdmin]

        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'me'] and self.request.user.is_staff:
            return AdminSerializer
        elif self.action == 'list':
            return UserListSerializer
        elif self.action == 'registration':
            return UserRegistrationSerializer
        elif self.action == 'partial_update':
            return AdminUpdateUserSerializer
        elif self.action == 'me':
            if self.request.method == 'PATCH':
                return UserUpdateSerializer
        elif self.action == 'destroy':
            return AdminDeleteSerializer
        elif self.action == 'activation':
            return UserActivationSerializer
        elif self.action == 'restore_password':
            return UserRestorePasswordSerializer
        
        return self.serializer_class

    @action(['post'], detail=False)
    def registration(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response('Check your email for complete registration.', status=status.HTTP_201_CREATED)
    
    
    @action(['get', 'patch'], detail=False, parser_classes=(MultiPartParser,))
    def me(self, request, *args, **kwargs):    
        self.get_object = self.request.user
        if request.method == 'GET':
            return self.retrieve(request, *args, **kwargs)
        elif request.method == 'PATCH':
            return self.partial_update(request, *args, **kwargs)
    
    @action(["post"], detail=False)
    def activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.is_active = True
        user.save()
        return Response('Registration complete.', status=status.HTTP_200_OK)
    
    @action(["post"], detail=False)
    def restore_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()
        send_new_password.delay(user.email, password)
        return Response('Email has been sent', status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        super().perform_update(serializer)
        user = serializer.instance
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        if instance == request.user:
            logout(self.request)
        self.perform_destroy(instance)
        return Response('user deleted.', status=status.HTTP_204_NO_CONTENT)
    
    def perform_create(self, serializer):
        user = serializer.save()
        secret_code = encode_uid(user.pk)
        send_activation_email.delay(user.email, secret_code)
