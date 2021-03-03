from datetime import date

from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class Institute(models.Model):
    name = models.CharField("Название института", default=None, max_length=50)

    class Meta:
        verbose_name = "Институт"
        verbose_name_plural = "Институты"

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField("Название группы", default=None, max_length=50)
    recruitment_date = models.DateField("Дата набора", default=date.today)
    institute_id = models.ForeignKey(Institute, verbose_name="Институт", on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.name

class Student(models.Model):
    date_of_enrollment = models.DateField("Дата зачисления", default=date.today)
    group_id = models.ForeignKey(Group, verbose_name="Группа", on_delete=models.CASCADE, null=False)
    #module_id = models.ManyToManyField(Module, verbose_name="Модули", related_name="student_module", blank=True)

    first_name = models.CharField(max_length=50, default=None, null=True, blank=True)
    last_name = models.CharField(max_length=50, default=None, null=True, blank=True)
    patronymic = models.CharField(max_length=50, default=None, null=True, blank=True)

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"

    def __str__(self):
        return str(self.group_id)

class Module(models.Model):
    name = models.CharField("Название модуля", default=None, max_length=50)
    student_id = models.ForeignKey(Student, verbose_name="Студент", on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "Модуль"
        verbose_name_plural = "Модули"

    def __str__(self):
        return self.name

class Point(models.Model):
    name = models.CharField("Название пункта", default=None, max_length=50)
    description = models.TextField("Описание", default=None, blank=True)
    file = models.ImageField("Файл", upload_to="Kemsu_Document/media/", blank=True)
    module_id = models.ForeignKey(Module, verbose_name="Модуль", on_delete=models.SET_NULL, null=True, blank=True)
    STATUS = (
        ('Не отправленно', 'но'),
        ('На подписании', 'нп'),
        ('Отказанно', 'о'),
        ('Подписанно', 'п'),
    )
    status = models.CharField(max_length=20, choices=STATUS, blank=True, default='Не отправленно', help_text='Статус документа')

    def create_module(self, name, description, module):
        self.name = name
        self.description = description
        self.module_id = module
        self.save()

    class Meta:
        verbose_name = "Пункт"
        verbose_name_plural = "Пункты"

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField("Название отдела", default=None, max_length=50)
    point_id = models.ForeignKey(Point, verbose_name="Пункт", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Отдел"
        verbose_name_plural = "Отделы"

    def __str__(self):
        return self.name

class Staff(models.Model):

    department_id = models.ForeignKey(Department, verbose_name="Отдел", on_delete=models.SET_NULL, null=True)

    first_name = models.CharField(max_length=50, default=None, null=True, blank=True)
    last_name = models.CharField(max_length=50, default=None, null=True, blank=True)
    patronymic = models.CharField(max_length=50, default=None, null=True, blank=True)

    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"

    def __str__(self):
        return str(self.department_id)


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

    def create_student(self, username, email, password=None, **extra_fields):
        # extra_fields.setdefault('is_student', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, email, password, **extra_fields)

    def create_staff(self, username, email, password=None, **extra_fields):
        # extra_fields.setdefault('is_student', False)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        #extra_fields.setdefault('is_student', False)

        #if extra_fields.get('is_staff') is not True:
        #    raise ValueError('Суперпользователь должен иметь is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=50, unique=True)
    email = models.EmailField(
        validators=[validators.validate_email],
        unique=True,
        blank=False
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    #is_student = models.BooleanField(default=False)

    staff_id = models.ForeignKey(Staff, verbose_name="Работник", on_delete=models.SET_NULL, null=True, blank=True)
    student_id = models.ForeignKey(Student, verbose_name="Студент", on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ('email',)

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username

    # def get_full_name(self):
    #     return self.last_name + " " + self.first_name + " " + self.patronymic
    #
    # def get_short_name(self):
    #     return self.last_name + " " + self.first_name