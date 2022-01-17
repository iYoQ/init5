from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS


class UserIsOwnerOrAdminOrReadOnly(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if type(obj) == type(user) and obj == user:
            return True
        return request.method in SAFE_METHODS or user.is_staff


class UserIsOwnerOrAdmin(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_staff or obj.pk == user.pk


class UserIsPostOwnerOrAdmin(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_staff or obj.author.pk == user.pk


class UserIsNewsmaker(IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.is_newsmaker


class ReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
