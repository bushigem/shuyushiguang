from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    """
    只允许超级管理员访问
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'super_admin'


class IsAdmin(permissions.BasePermission):
    """
    只允许管理员访问
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin


class IsAdminOrSelf(permissions.BasePermission):
    """
    只允许管理员或用户自己访问
    """
    def has_object_permission(self, request, view, obj):
        # 管理员可以访问任何用户
        if request.user.is_admin:
            return True
        
        # 用户可以访问自己的信息
        return obj.id == request.user.id