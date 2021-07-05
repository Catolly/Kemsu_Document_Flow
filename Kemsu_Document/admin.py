from django.contrib import admin
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.token_blacklist import admin as ad
from .models import (
    Department, Group, Institute, BypassSheet,
    Point, User, Statement, Staff, Student, RequiredDocuments, UploadedDocuments, BypassSheetTemplate,
    StatementsTemplate, PointTemplate, RequiredDocumentsTemplate, UploadDocumentsFormat, Deadline
)

# Register your models here.

class OutstandingTokenAdmin(ad.OutstandingTokenAdmin):

    def has_delete_permission(self, *args, **kwargs):
        return True

admin.site.register(User)
admin.site.register(Department)
admin.site.register(Institute)
admin.site.register(BypassSheet)
admin.site.register(Point)
admin.site.register(Statement)
admin.site.register(Staff)
admin.site.register(Student)
admin.site.register(RequiredDocuments)
admin.site.register(UploadedDocuments)
admin.site.register(BypassSheetTemplate)
admin.site.register(StatementsTemplate)
admin.site.register(PointTemplate)
admin.site.register(RequiredDocumentsTemplate)
admin.site.register(UploadDocumentsFormat)
admin.site.unregister(OutstandingToken)
admin.site.register(OutstandingToken, OutstandingTokenAdmin)
admin.site.register(Group)
admin.site.register(Deadline)