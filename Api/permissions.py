from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser


class ApiPermissions(permissions.BasePermission):
    get_permission = None
    put_permission = None
    post_permission = None
    patch_permission = None
    delete_permission = None
    option_permission = 'IsAdmin'

    def has_object_permission(self, request, view, obj):
        permission_name = f'{request.method.lower()}_permission'
        permission = getattr(view, permission_name)
        if permission == 'IsAuthorised':
            return type(request.user) is not AnonymousUser
        if permission == 'IsNotAuthorised':
            return type(request.user) is AnonymousUser or request.user.id == obj.id or request.user.groups.filter(name='Judges').exists() or request.user.is_superuser == True
        elif permission == 'IsOwner':
            return request.user.id == obj.id or request.user.groups.filter(name='Judges').exists() or request.user.is_superuser == True
        elif permission == 'IsJudge':
            return request.user.groups.filter(name='Judges').exists() or (request.user.is_superuser == True)
        elif permission == 'IsAdmin':
            return request.user.is_superuser == True

#te linijki są spowodowane faktem, że dla profilu, zgłoszenia i dla turnieju nie zadziała zwykłe "request.user.id == obj.id"
        elif permission == 'IsProfileOwner':
            if type(request.user) is AnonymousUser:
                return False
            else:
                return (request.user.email == obj.user.email) or request.user.is_superuser == True
        elif permission == 'IsNotificationOwner':
            if type(request.user) is AnonymousUser:
                return False
            else:
                return (request.user.email == obj.player.user.email) or request.user.groups.filter(name='Judges').exists() or request.user.is_superuser == True
        elif permission == 'IsTournamentJudge':
            if type(request.user) is AnonymousUser:
                return False
            else:
                return (request.user.email == obj.judge.user.email) or request.user.is_superuser == True
        else:
            return False