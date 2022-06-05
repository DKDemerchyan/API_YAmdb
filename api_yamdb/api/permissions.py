from rest_framework import permissions


class IsAdminOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff or request.user.role == 'admin':
            return True


class IsAdminOrReadOnly(permissions.BasePermission):

    # def has_permission(self, request, view):
    #     if not request.user.is_authenticated:
    #         return False
    #     if request.user.is_staff or request.user.role == 'admin':
    #         return True
    #
    # def has_object_permission(self, request, view, obj):
    #     if request.user.is_staff or request.user.role == 'admin':
    #         return True

    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.role == 'admin'
        )


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authentificated
        )
