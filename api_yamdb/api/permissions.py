from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or bool(request.user and request.user.is_staff))


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class AdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.role == request.user.ADMIN
                or request.user.is_superuser
            )
        )


class AuthorOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return obj == request.user
