from rest_framework.permissions import BasePermission


class HasPositiveBalance(BasePermission):
    message = "You do not have a positive balance to use the API."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.balance > 0
