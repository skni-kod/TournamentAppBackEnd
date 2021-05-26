from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser, User
from Api.models import CustomUser


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


class IsAuthorisedAndOwner(permissions.BasePermission):
    # 'You must be the owner of this object.'
    def has_permission(self, request, view):
        return bool(type(request.user) is not AnonymousUser)
    def has_object_permission(self, request, view, obj):
        return (request.user.email == obj.user.email or request.user.is_superuser == True)


class IsPlayer(permissions.BasePermission):    
    # 'You have to be Player'
    def has_permission(self, request, view):
        return bool( ((type(request.user) is not AnonymousUser)  and request.user.permissions == 'Player') or request.user.is_superuser == True)


class IsJudge(permissions.BasePermission):    
    # 'You have to be Judge'
    def has_permission(self, request, view):
        return bool( ((type(request.user) is not AnonymousUser)  and request.user.permissions == 'Judge') or request.user.is_superuser == True)


class IsAdmin(permissions.BasePermission):    
    # 'You have to be admin - to have superuser extrafield set to True'
    def has_permission(self, request, view):
        return bool( (type(request.user) is not AnonymousUser)  and request.user.is_superuser == True)

        
class IsTournamentJudge(permissions.BasePermission):    
    # 'You have to be tournament's Judge'
    def has_permission(self, request, view):
        return bool( ((type(request.user) is not AnonymousUser)  and request.user.permissions == 'Judge') or request.user.is_superuser == True)
    def has_object_permission(self, request, view, obj):
        return (request.user.email == obj.judge.user.email)


class IsGameJudge(permissions.BasePermission):    
    # 'You have to be Judge of game's tournament'
    def has_permission(self, request, view):
        return bool( ((type(request.user) is not AnonymousUser)  and request.user.permissions == 'Judge') or request.user.is_superuser == True)
    def has_object_permission(self, request, view, obj):
        return (request.user.email == obj.tournament.judge.user.email)

 
class IsResultJudge(permissions.BasePermission):    
    # 'You have to be Judge of result's tournament'
    def has_permission(self, request, view):
        return bool( ((type(request.user) is not AnonymousUser)  and request.user.permissions == 'Judge') or request.user.is_superuser == True)
    def has_object_permission(self, request, view, obj):
        return (request.user.email == obj.tournament.judge.user.email or request.method in permissions.SAFE_METHODS)             


class IsNotificationOwner(permissions.BasePermission):    
    # 'You have to be Judge of game's tournament'
    def has_permission(self, request, view):
        return bool( ((type(request.user) is not AnonymousUser)  and request.user.permissions == 'Player') or request.user.is_superuser == True)
    def has_object_permission(self, request, view, obj):
        return (request.user.email == obj.notification.player.user.email)


class IsUserOwner(permissions.BasePermission):    
    # 'You have to be Judge of game's tournament'
    def has_permission(self, request, view):
        return bool( (type(request.user) is not AnonymousUser)   or request.user.is_superuser == True)
    def has_object_permission(self, request, view, obj):
        return (request.user.email == obj.email)


class IsProfileOwner(permissions.BasePermission):    
    # 'You have to be Judge of game's tournament'
    def has_permission(self, request, view):
        return bool( (type(request.user) is not AnonymousUser)   or request.user.is_superuser == True)
    def has_object_permission(self, request, view, obj):
        return (request.user.email == obj.user.email)
