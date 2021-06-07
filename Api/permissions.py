from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser


class IsReadOnly(permissions.BasePermission):
   # 'View must be read-only'
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_superuser == True


class IsAuthorised(permissions.BasePermission):
    # 'You must be Authorised.'
    def has_permission(self, request, view,):
        return bool(type(request.user) is not AnonymousUser)


class IsNotAuthorised(permissions.BasePermission):
    # 'You cant be Authorised.'
    def has_permission(self, request, view,):
        return bool(type(request.user) is AnonymousUser)


class IsPlayer(permissions.BasePermission):    
    # 'You have to be Player'
    def has_permission(self, request, view):
        return bool( ( (type(request.user) is not AnonymousUser)  and request.user.groups.filter(name='Players').exists() ) or request.user.is_superuser == True)
        

class IsJudge(permissions.BasePermission):    
    # 'You have to be Judge'
    def has_permission(self, request, view):
        return bool( ((type(request.user) is not AnonymousUser)  and request.user.groups.filter(name='Judges').exists() ) or request.user.is_superuser == True)


class IsAdmin(permissions.BasePermission):    
    # 'You have to be admin - to have superuser extrafield set to True'
    def has_permission(self, request, view):
        return bool( (type(request.user) is not AnonymousUser)  and request.user.is_superuser == True)
