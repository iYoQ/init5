from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth import logout
from rest_framework.decorators import action
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
from ..general.paginations import UserPaginaton
from .serializers import *


class UserViewSet(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPaginaton
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
        elif self.action == 'registration':
            return UserRegistrationSerializer
        elif self.action == 'partial_update':
            return AdminUpdateUserSerializer
        elif self.action == 'me':
            if self.request.method == 'PATCH':
                return UpdateUserSerializer
        elif self.action == 'destroy':
            return AdminDeleteSerializer
        
        return self.serializer_class

    @action(['post'], detail=False)
    def registration(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(['get', 'patch'], detail=False)
    def me(self, request, *args, **kwargs):    
        self.get_object = self.request.user
        if request.method == 'GET':
            return self.retrieve(request, *args, **kwargs)
        elif request.method == 'PATCH':
            return self.partial_update(request, *args, **kwargs)

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
        serializer.save()
