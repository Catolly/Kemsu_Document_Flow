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