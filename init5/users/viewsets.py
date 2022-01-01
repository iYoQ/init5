from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from django.contrib.auth import logout
from .permissions import *
from .models import User
from .serializers import *


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'head', 'patch', 'options', 'delete']


    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [ReadOnly]
        elif self.action in ['partial_update', 'destroy']:
            self.permission_classes = [UserIsOwnerOrAdminOrReadOnly]
        elif self.action in ['destroy']:
            self.permission_classes = [UserIsOwnerOrAdmin]
        elif self.action == 'me':
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'me'] and self.request.user.is_superuser:
            return AdminUserSerializer
        elif self.action == 'registration':
            return UserRegistrationSerializer
        elif self.action == 'partial_update':
            if self.request.user.is_superuser:
                return AdminUpdateUserSerializer
            return UpdateUserSerializer
        elif self.action == 'destroy' or (self.action == 'me' and self.request and self.request.method == 'DELETE'):
            return UserDeleteSerializer
        
        return self.serializer_class

    @action(['post'], detail=False)
    def registration(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('account created', status=status.HTTP_201_CREATED)
        return Response('invalid data', status=status.HTTP_400_BAD_REQUEST)
    
    @action(['get', 'patch', 'delete'], detail=False)
    def me(self, request, *args, **kwargs):    
        self.get_object = self.request.user
        if request.method == 'GET':
            return self.retrieve(request, *args, **kwargs)
        elif request.method == 'PATCH':
            return self.partial_update(request, *args, **kwargs)
        elif request.method == 'DELETE':
            return self.destroy(request, *args, **kwargs)

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

