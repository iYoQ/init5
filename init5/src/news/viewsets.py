from rest_framework import status, filters
from rest_framework.response import Response
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
from .models import News
from ..general.serializers import AdminDeleteSerializer
from ..general.paginations import PostPaginaton
from .serializers import *


class NewsViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    pagination_class = PostPaginaton
    search_fields = ['headline']
    http_method_names = ['get', 'post', 'head', 'patch', 'options', 'delete']

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = News.objects.all()
        else:
            queryset = News.objects.filter(active=True)
        return queryset

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [custom_permissions.UserIsNewsmaker]
        elif self.action == 'partial_update':
            self.permission_classes = [custom_permissions.UserIsPostOwnerOrAdmin]
        elif self.action == 'destroy':
            self.permission_classes = [IsAdminUser]

        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.user.is_staff:
            if self.action == 'list':
                return AdminListSerializer
            if self.action == 'retrieve':
                return AdminDetailSerializer
            if self.action == 'partial_update':
                return AdminUpdateSerializer

        elif self.action in ['create', 'partial_update']:
            return NewsCreateUpdateSerializer
        elif self.action == 'destroy':
            return AdminDeleteSerializer
        elif self.action == 'list':
            return NewsListSerializer
        
        return self.serializer_class
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)