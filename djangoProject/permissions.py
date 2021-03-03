from rest_framework.permissions import BasePermission

class IsStudentUser(BasePermission):

    def has_permission(self, request, view):

        #pk = GetBypassSheetsView.pk

        return bool(request.user) #and request.user.student_id==pk)