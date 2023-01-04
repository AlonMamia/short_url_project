from rest_framework import permissions


class AllowedMethods(permissions.BasePermission):
    """
    Global permission to disallow all requests for unauthorized methods.
    """
    ALLOWED_METHODS = ['GET', 'POST']

    def has_permission(self, request, view):
        return request.method in self.ALLOWED_METHODS
