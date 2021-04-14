from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions

''' для памятки
        STATUS = (
        ('Работник', 'работник'),
        ('Студент', 'студент'),
        ('Администратор', 'администратор'),
'''

class PermissionIsStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.status == "Студент")

class PermissionIsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.status == "Администратор")

class PermissionIsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.status == "Работник")

class IsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.status == "Работник")

class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.status == "Администратор")

class IsStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.status == "Студент" and request.user.id == view.kwargs['pk'])

class StudentListViewPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and (request.user and request.user.status == "Студент" and request.user.id == view.kwargs['pk'])
                    or (request.user and request.user.status == "Администратор")
                    or (request.user and request.user.status == "Работник"))

class PatchUserDataPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool((request.user and request.user.status == "Студент" and request.user.id == view.kwargs['pk'])
                    or (request.user and request.user.status == "Администратор"))

class BypassSheetsViewPermission(permissions.BasePermission):

     def has_permission(self, request, view):
         return bool(request.user and request.user.status == "Студент")
