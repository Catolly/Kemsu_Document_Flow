from django.db import models
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    middle_name = models.CharField(max_length=75)
    #role_in_the_system = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    e_mail = models.EmailField()
    #link_on_Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    #link_on_Employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    #link_on_Administrator = models.ForeignKey(Administrator, on_delete=models.CASCADE)

class Administrator(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=75)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.IntegerField()
    direction_of_study = models.CharField(max_length=75)
    institute = models.CharField(max_length=75)
    group = models.CharField(max_length=30)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)

class Document(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=75)
    #point = models.CharField(max_length=75)
    # data = models.CharField(max_length=75)
    link_on_Student = models.ForeignKey(Student, on_delete=models.CASCADE)

class Point(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=75)
    description = models.TextField()
    file = models.FileField()
    link_on_module = models.ForeignKey(Document, on_delete=models.CASCADE)

@staticmethod
def create_user(first_name, last_name, middle_name, e_mail, password, **any_arguments):
    user = Users()
    user.first_name = first_name
    user.last_name = last_name
    user.middle_name = middle_name
    user.e_mail = e_mail
    user.set_password(user, password)
    user.save()

@staticmethod
def set_password(user, raw_password):
    user.password = make_password(raw_password)

