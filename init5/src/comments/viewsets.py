from django.apps import AppConfig
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin, 
    UpdateModelMixin, 
    DestroyModelMixin, 
    ListModelMixin
)

import src.general.permissions as custom_permissions
from .models import (
    ArticleComment,
    NewsComment
)
from .serializers import *


class CommentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'head', 'patch', 'options', 'delete']

    def get_permissions(self):
        if self.action == 'change_rating':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'partial_update':
            self.permission_classes = [custom_permissions.UserIsPostOwnerOrAdmin]
        elif self.action == 'destroy':
            self.permission_classes = [custom_permissions.UserIsPostOwnerOrAdmin]
        
        return super().get_permissions()
    
    @action(['patch'], detail=True)
    def change_rating(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


class ArticleCommentViewSet(CommentViewSet):
    serializer_class = ArticleCommentSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = ArticleComment.objects.filter(article=self.kwargs['article_id'])
        else:
            queryset = ArticleComment.objects.filter(article=self.kwargs['article_id'], active=True)
        return queryset

    def get_serializer_class(self):
        if self.action == 'change_rating':
            return ArticleCommentChangeRatingSerializer
        return super().get_serializer_class()
    

class NewsCommentViewSet(CommentViewSet):
    serializer_class = NewsCommentSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = NewsComment.objects.filter(news=self.kwargs['news_id'])
        else:
            queryset = NewsComment.objects.filter(news=self.kwargs['news_id'], active=True)
        return queryset

    def get_serializer_class(self):
        if self.action == 'change_rating':
            return NewsCommentChangeRatingSerializer
        return super().get_serializer_class()