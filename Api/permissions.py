from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser


class IsAdminOrReadOnly(permissions.BasePermission):
    # 'View must be read-only'
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_superuser is True


class IsAuthorised(permissions.BasePermission):
    # 'You must be Authorised.'
    def has_permission(self, request, view):
        return type(request.user) is not AnonymousUser and request.method in permissions.SAFE_METHODS


class IsNotAuthorised(permissions.BasePermission):
    # 'You cant be Authorised.'
    def has_permission(self, request, view):
        return type(request.user) is AnonymousUser


class IsPlayer(permissions.BasePermission):
    # 'You have to be Player'
    def has_permission(self, request, view):
        return bool(((type(request.user) is not AnonymousUser) and request.user.groups.filter(
            name='Players').exists()) or request.user.is_superuser == True)


class IsJudgeOrAdmin(permissions.BasePermission):
    # 'You have to be Judge or Admin'
    def has_permission(self, request, view):
        return ((type(request.user) is not AnonymousUser) and request.user.groups.filter(
            name='Judges').exists()) or request.user.is_superuser == True


class IsAdmin(permissions.BasePermission):
    # 'You have to be admin - to have superuser extrafield set to True'
    def has_permission(self, request, view):
        return bool((type(request.user) is not AnonymousUser) and request.user.is_superuser == True)
