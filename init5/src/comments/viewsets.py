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

    def get_queryset(self):
        model = self.model
        if self.request.user.is_staff:
            queryset = model.objects.all()
        else:
            queryset = model.objects.filter(active=True)
        return queryset

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

    @property
    def model(self):
        return ArticleComment

    def get_serializer_class(self):
        if self.action == 'change_rating':
            return ArticleCommentChangeRatingSerializer
        return super().get_serializer_class()

class NewsCommentViewSet(CommentViewSet):
    serializer_class = NewsCommentSerializer

    @property
    def model(self):
        return NewsComment

    def get_serializer_class(self):
        if self.action == 'change_rating':
            return NewsCommentChangeRatingSerializer
        return super().get_serializer_class()