from rest_framework import permissions

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

class StudentViewPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method == "GET":
                return bool((request.user and request.user.status == "Студент" and request.user.id == view.kwargs['pk'])
                            or (request.user and request.user.status == "Администратор")
                            or (request.user and request.user.status == "Работник"))
            elif request.method == "PATCH":
                return bool((request.user and request.user.status == "Студент" and request.user.id == view.kwargs['pk'])
                            or (request.user and request.user.status == "Администратор"))
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
