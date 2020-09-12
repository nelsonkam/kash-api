from rest_framework.permissions import BasePermission


class IsCurrentShopOwner(BasePermission):

    def has_permission(self, request, view):
        return request.shop and request.shop.user == request.user
