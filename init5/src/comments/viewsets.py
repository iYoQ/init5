from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from ..general.paginations import CommentsPagination
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
    pagination_class = CommentsPagination

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
    
    def create(self, data, *args, **kwargs):
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        if news := serializer.validated_data.get('news'):
            post_url = news.get_absolute_url()
        elif article := serializer.validated_data.get('article'):
            post_url = article.get_absolute_url()
        serializer.save(author=self.request.user, post_url=post_url)
    
    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


class ArticleCommentViewSet(CommentViewSet):
    serializer_class = ArticleCommentSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = ArticleComment.objects.filter(article=self.kwargs.get('article_id'))
        else:
            queryset = ArticleComment.objects.filter(article=self.kwargs.get('article_id'), active=True)
        return queryset

    def get_serializer_class(self):
        if self.action == 'change_rating':
            return ArticleCommentChangeRatingSerializer
        return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data.update({'article': kwargs['article_id']})
        return super().create(data, *args, **kwargs)

class NewsCommentViewSet(CommentViewSet):
    serializer_class = NewsCommentSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = NewsComment.objects.filter(news=self.kwargs.get('news_id'))
        else:
            queryset = NewsComment.objects.filter(news=self.kwargs.get('news_id'), active=True)
        return queryset

    def get_serializer_class(self):
        if self.action == 'change_rating':
            return NewsCommentChangeRatingSerializer
        return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data.update({'news': kwargs['news_id']})
        return super().create(data, *args, **kwargs)


class UserCommentsViewSet(ListModelMixin, GenericViewSet):
    serializer_class = UserCommentsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CommentsPagination

    def get_queryset(self):
        qs_articles_comments = ArticleComment.objects.filter(author__username=self.kwargs.get('username')).select_related('author')
        qs_news_comments = NewsComment.objects.filter(author__username=self.kwargs.get('username')).select_related('author')
        qs_comments = qs_articles_comments.union(qs_news_comments)
        return qs_comments.order_by('-date_create')
