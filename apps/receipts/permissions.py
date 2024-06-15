from rest_framework import permissions


class IsOwnerOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        # Allow GET requests only if the user is authenticated
        if request.method == "GET":
            return request.user.is_authenticated

        # For other methods (POST, PUT, DELETE), always check object permissions
        return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are only allowed to the owner of the receipt.
        return obj.user == request.user
