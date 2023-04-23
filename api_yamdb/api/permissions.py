from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class AdminModeratAuthorOrReadonly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role == User.ADMIN
            or request.user.is_superuser
            or request.user.role == User.MODERATOR
        )


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
