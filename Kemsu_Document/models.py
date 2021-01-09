from django.contrib.auth import user_logged_in
from django.db import models
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
from django.http import HttpResponse

from django.utils.crypto import get_random_string, salted_hmac
from django.conf import settings
SESSION_KEY = '_student_id_id'

'''class Users(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    middle_name = models.CharField(max_length=75)
    #role_in_the_system = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    e_mail = models.EmailField()
    #link_on_Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    #link_on_Employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    #link_on_Administrator = models.ForeignKey(Administrator, on_delete=models.CASCADE)'''

'''class Administrator(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)'''

class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=75)

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    middle_name = models.CharField(max_length=75)
    # role_in_the_system = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    e_mail = models.EmailField()

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    middle_name = models.CharField(max_length=75)
    password = models.CharField(max_length=128)
    e_mail = models.EmailField()
    course = models.IntegerField()
    direction_of_study = models.CharField(max_length=75)
    institute = models.CharField(max_length=75)
    group = models.CharField(max_length=30)

class Document(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=75)
    #point = models.CharField(max_length=75)
    # data = models.CharField(max_length=75)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)

class Point(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=75)
    description = models.TextField()
    file = models.FileField()
    link_on_module = models.ForeignKey(Document, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)

def create_employee(first_name, last_name, middle_name, e_mail, password, department_name):
    user = Employee()
    user.first_name = first_name
    user.last_name = last_name
    user.middle_name = middle_name
    user.e_mail = e_mail
    user.department_id = Department.objects.get(name=department_name)
    set_password(user, password)
    user.save()

def create_student(first_name, last_name, middle_name, e_mail, password, course, direction_of_study, institute, group):
    user = Student()
    user.first_name = first_name
    user.last_name = last_name
    user.middle_name = middle_name
    user.e_mail = e_mail
    set_password(user, password)
    user.course = course
    user.direction_of_study = direction_of_study
    user.institute = institute
    user.group = group
    user.save()

def set_password(user, raw_password):
    user.password = make_password(raw_password)

def authenticate(e_mail, password):
    user = Student.objects.get(e_mail=e_mail)
    if user is not None and check_password(password, user.password):
        return user