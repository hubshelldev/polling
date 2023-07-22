from rest_framework import permissions
from django.contrib import auth

class ISEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return str(request.user.roles) in ["Employee"]

class ISSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return str(request.user.roles) in ["SuperAdmin"]

