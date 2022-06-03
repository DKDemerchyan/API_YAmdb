from rest_framework import permissions


class IsSuperUserOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # return (request.user.username =='superuser' or
        #     request.method in permissions.SAFE_METHODS)
        if request.user.username in ['superuser', 'admin', 'moderator'] or request.method in permissions.SAFE_METHODS:
            return True



    # def has_permission(self, request, view):
