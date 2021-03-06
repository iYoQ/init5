from rest_framework import filters
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
    CreateModelMixin,
    RetrieveModelMixin, 
    UpdateModelMixin, 
    DestroyModelMixin, 
    ListModelMixin
)

import src.general.permissions as custom_permissions
from .models import Article, Category
from ..general.serializers import AdminDeleteSerializer
from ..general.paginations import PostPagination
from .serializers import *


class ArticleViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = PostPagination
    filter_fields = ['category']
    search_fields = ['headline']
    ordering_fields = ['date_create']
    ordering = ['-date_create']
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'head', 'patch', 'options', 'delete']

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Article.objects.all()
        else:
            queryset = Article.objects.filter(active=True)
        return queryset

    def get_permissions(self):
        if self.action in ['create', 'change_rating']:
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'partial_update':
            self.permission_classes = [custom_permissions.UserIsPostOwnerOrAdmin]

        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.user.is_staff:
            if self.action == 'list':
                return AdminListSerializer
            if self.action == 'retrieve':
                return AdminDetailSerializer
            if self.action == 'partial_update':
                return AdminUpdateSerializer

        if self.action in ['create', 'partial_update']:
            return ArticleCreateUpdateSerializer
        elif self.action == 'destroy':
            return AdminDeleteSerializer
        elif self.action == 'change_rating':
            return ArticleChangeRatingSerializer
        elif self.action in ['list', 'top']:
            return ArticleListSerializer
        
        return self.serializer_class
    
    @action(['patch'], detail=True)
    def change_rating(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    @action(['get'], detail=False)
    def top(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('-rating')[:5]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserArticlesList(ListModelMixin, GenericViewSet):
    serializer_class = ArticleListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = PostPagination
    search_fields = ['headline']
    ordering_fields = ['date_create']
    ordering = ['-date_create']

    def get_queryset(self):
        return Article.objects.filter(author__username=self.kwargs.get('username')).select_related('author')


class CategoryViewSet(ListModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'name'
