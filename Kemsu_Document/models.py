import jwt

from datetime import datetime
from datetime import timedelta

from django.contrib.auth import user_logged_in
from django.db import models
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
from django.core import validators
from django.http import HttpResponse
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.crypto import get_random_string, salted_hmac
from django.conf import settings
from django.contrib.auth.models import BaseUserManager

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

'''class Department(models.Model):
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
    e_mail = models.EmailField()'''

class UserManager(BaseUserManager):
    def _create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Указанное имя пользователя должно быть установлено')

        if not email:
            raise ValueError('Данный адрес электронной почты должен быть установлен')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_student', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, email, password, **extra_fields)

    def create_staff(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_student', False)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_student', False)

        #if extra_fields.get('is_staff') is not True:
        #    raise ValueError('Суперпользователь должен иметь is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    '''id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    middle_name = models.CharField(max_length=75)
    password = models.CharField(max_length=128)
    e_mail = models.EmailField()
    course = models.IntegerField()
    direction_of_study = models.CharField(max_length=75)
    institute = models.CharField(max_length=75)
    group = models.CharField(max_length=30)'''
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(
        validators=[validators.validate_email],
        unique=True,
        blank=False
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_student = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    #REQUIRED_FIELDS = ()

    objects = UserManager()

    def __str__(self):
        return self.username

    # @property
    # def token(self):
    #     return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    # def _generate_jwt_token(self):
    #     dt = datetime.now() + timedelta(minutes=10)
    #     token = jwt.encode({
    #         'id': self.pk,
    #         'exp': int(dt.strftime('%S')),
    #         'is_staff': self.is_staff,
    #         'is_superuser' : self.is_superuser
    #     }, settings.SECRET_KEY, algorithm='HS256')
    #
    #     #return token.encode().decode('utf-8')
    #     return token

'''class Document(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=75)
    #point = models.CharField(max_length=75)
    # data = models.CharField(max_length=75)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)'''

'''class Point(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=75)
    description = models.TextField()
    file = models.FileField()
    link_on_module = models.ForeignKey(Document, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)'''

'''def create_employee(first_name, last_name, middle_name, e_mail, password, department_name):
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
        return user '''