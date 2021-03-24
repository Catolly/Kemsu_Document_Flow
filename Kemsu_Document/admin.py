from django.contrib import admin
from .models import (
    Department, Group, Institute, Module,
    Point, User, Statement, Staff, Student
)

# Register your models here.

admin.site.register(User)
admin.site.register(Department)
admin.site.register(Group)
admin.site.register(Institute)
admin.site.register(Module)
admin.site.register(Point)
admin.site.register(Statement)
admin.site.register(Staff)
admin.site.register(Student)