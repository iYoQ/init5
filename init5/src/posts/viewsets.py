from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from src.users.serializers import AdminDeleteSerializer
from rest_framework.permissions import (
    IsAdminUser, 
    IsAuthenticated, 
    IsAuthenticatedOrReadOnly
)
from .models import (
    Post,
    Comment
)
from .serializers import *
import src.users.permissions as custom_permissions


class PostViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'head', 'patch', 'options', 'delete']

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [custom_permissions.ReadOnly]
        elif self.action in ['create_article', 'change_rating']:
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'create_news':
            self.permission_classes = [custom_permissions.UserIsNewsmaker]
        elif self.action == 'partial_update':
            self.permission_classes = [custom_permissions.UserIsPostOwnerOrAdmin]
        elif self.action == 'destroy':
            self.permission_classes = [IsAdminUser]

        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create_article':
            return ArticleCreateSerializer
        elif self.action == 'create_news':
            return NewsCreateSerializer
        elif self.action == 'change_rating':
            return ChangeRatingSerializer
        elif self.action == 'partial_update':
            return UpdateSerializer
        elif self.action == 'destroy':
            return AdminDeleteSerializer
        
        return self.serializer_class
    
    @action(['patch'], detail=True)
    def change_rating(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ArticleViewSet(PostViewSet):
    queryset = Post.objects.filter(is_article=True)
    serializer_class = ArticleSerializer

    @action(['post'], detail=False)
    def create_article(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class NewsViewSet(PostViewSet):
    queryset = Post.objects.filter(is_news=True)
    serializer_class = NewsSerializer

    @action(['post'], detail=False)
    def create_news(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
