from rest_framework.permissions import BasePermission, SAFE_METHODS


class UserIsOwnerOrAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_superuser or obj.pk == user.pk


class UserIsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_superuser or obj.pk == user.pk


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS