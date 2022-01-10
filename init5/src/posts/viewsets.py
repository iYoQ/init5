from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import (
    IsAdminUser, 
    IsAuthenticated, 
    IsAuthenticatedOrReadOnly
)
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin, 
    UpdateModelMixin, 
    DestroyModelMixin, 
    ListModelMixin
)

import src.general.permissions as custom_permissions
from .models import (
    Article,
    News,
    ArticleComment,
    NewsComment
)
from src.users.serializers import AdminDeleteSerializer
from .serializers import *


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
        elif self.action == 'destroy':
            return AdminDeleteSerializer
        
        return self.serializer_class
    
    @action(['patch'], detail=True)
    def change_rating(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ArticleViewSet(PostViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return ArticleUpdateSerializer
        elif self.action == 'change_rating':
            return ArticleChangeRatingSerializer
        return super().get_serializer_class()

    @action(['post'], detail=False)
    def create_article(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class NewsViewSet(PostViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return NewsUpdateSerializer
        elif self.action == 'change_rating':
            return NewsChangeRatingSerializer
        return super().get_serializer_class()

    @action(['post'], detail=False)
    def create_news(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CommentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'head', 'patch', 'options', 'delete']

    def get_permissions(self):
        if self.action == 'partial_update':
            self.permission_classes = [custom_permissions.UserIsPostOwnerOrAdmin]
        elif self.action == 'destroy':
            self.permission_classes = [custom_permissions.UserIsPostOwnerOrAdmin]

        return super().get_permissions()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


class ArticleCommentViewSet(CommentViewSet):
    queryset = ArticleComment.objects.all()
    serializer_class = CreateArticleCommentSerializer


class NewsCommentViewSet(CommentViewSet):
    queryset = NewsComment.objects.all()
    serializer_class = CreateNewsCommentSerializer
