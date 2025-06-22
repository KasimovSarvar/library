from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return getattr(request, "user_role", None) == 0

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return getattr(request, "user_role", None) == 1
