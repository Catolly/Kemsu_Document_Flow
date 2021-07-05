from rest_framework import permissions

from Kemsu_Document.models import Staff, Student


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

class UserViewPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method == "GET":
                return bool((request.user and request.user.status == "Студент" and request.user.id == view.kwargs['pk'])
                            or(request.user and request.user.status == "Администратор")
                            or (request.user and request.user.status == "Работник"))
            elif request.method == "PATCH":
                return bool((request.user and request.user.status == "Студент" and request.user.id == view.kwargs['pk'])
                            or (request.user and request.user.status == "Администратор")
                            or (request.user and request.user.status == "Работник" and request.user.id == view.kwargs['pk']))
            return False
        return False

class BypassSheetsViewPermission(permissions.BasePermission):

     def has_permission(self, request, view):
         if request.method == "GET":
             if request.user.is_authenticated:
                return bool((request.user and request.user.status == "Студент")
                                or (request.user and request.user.status == "Администратор")
                                or (request.user and request.user.status == "Работник"))
         elif request.method == "POST":
            if request.user.is_authenticated:
                return bool(request.user and request.user.status == "Студент")
         elif request.method == "PATCH":
             if request.user.is_authenticated:
                 return bool(request.user and request.user.status == "Работник" and
                             Staff.objects.get(user=request.user).department.title == request.GET.get('department', ''))

class BypassSheetViewPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool((request.user and request.user.status == "Студент")
                        or (request.user and request.user.status == "Администратор")
                        or (request.user and request.user.status == "Работник"))

class UsersViewPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool((request.user and request.user.status == "Администратор")
                        or (request.user and request.user.status == "Работник"))

class BanUnbanPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user and request.user.status == "Администратор")

class UploadDocumentsPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user and request.user.status == "Студент")

class DepartmentViewPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool((request.user and request.user.status == "Студент")
                        or (request.user and request.user.status == "Работник")
                        or (request.user and request.user.status == "Администратор"))

class GroupViewPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool((request.user and request.user.status == "Работник")
                        or (request.user and request.user.status == "Администратор"))

class BypassSheetTemplateViewPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == "GET":
            if request.user.is_authenticated:
                return bool(request.user)
        else:
            if request.user.is_authenticated:
                return bool(request.user and request.user.status == "Администратор")

class UploadStudentsPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user and request.user.is_superuser == True)

class UpdateBypassSheetSchemaDeadline(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user and request.user.status == 'Работник')

class GetBypassSheetsSchemaDeadline(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user and request.user.status == 'Работник')