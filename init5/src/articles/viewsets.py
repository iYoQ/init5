from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (
    IsAdminUser, 
    IsAuthenticated, 
    IsAuthenticatedOrReadOnly
)
from rest_framework.mixins import (
    RetrieveModelMixin, 
    UpdateModelMixin, 
    DestroyModelMixin, 
    ListModelMixin
)

import src.general.permissions as custom_permissions
from .models import Article
from ..general.serializers import AdminDeleteSerializer
from .serializers import *


class ArticleViewSet(RetrieveModelMixin, UpdateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ['category', 'rating', ]
    search_fields = ['headline']
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'head', 'patch', 'options', 'delete']

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Article.objects.all()
        else:
            queryset = Article.objects.filter(active=True)
        return queryset

    def get_permissions(self):
        if self.action in ['create_article', 'change_rating']:
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'partial_update':
            self.permission_classes = [custom_permissions.UserIsPostOwnerOrAdmin]

        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.user.is_staff:
            if self.action == 'list':
                return AdminListSerializer
            return AdminDetailSerializer
        elif self.action in ['create_article', 'partial_update']:
            return ArticleCreateUpdateSerializer
        elif self.action == 'destroy':
            return AdminDeleteSerializer
        elif self.action == 'change_rating':
            return ArticleChangeRatingSerializer
        elif self.action == 'list':
            return ArticleListSerializer
        
        return self.serializer_class
    
    @action(['patch'], detail=True)
    def change_rating(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    @action(['post'], detail=False)
    def create_article(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    
