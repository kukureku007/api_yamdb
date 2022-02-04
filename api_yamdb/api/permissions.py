from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or bool(request.user.is_authenticated
            and (  request.user.role == request.user.ADMIN
                or request.user.is_superuser
            )))



class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class AdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
<<<<<<< HEAD
            request.user.is_authenticated and (
=======
            request.user.is_authenticated
            and (
>>>>>>> 6641783050c14c6b2260ee0e6365e39a9f70ab88
                request.user.role == request.user.ADMIN
                or request.user.is_superuser
            )
        )
<<<<<<< HEAD
=======


class AuthorOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return obj == request.user
>>>>>>> 6641783050c14c6b2260ee0e6365e39a9f70ab88
