from datetime import date

from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class Institute(models.Model):
    title = models.CharField("Название института", default=None, max_length=50)

    class Meta:
        verbose_name = "Институт"
        verbose_name_plural = "Институты"

    def __str__(self):
        return self.title

class Group(models.Model):
    title = models.CharField("Название группы", default=None, max_length=50, unique=True)
    recruitment_date = models.DateField("Дата набора", default=date.today)
    institute = models.ForeignKey(Institute, verbose_name="Институт", on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.title

class Department(models.Model):
    title = models.CharField("Название отдела", default=None, max_length=100)
    institute = models.ForeignKey(Institute, verbose_name= "Институт", on_delete=models.CASCADE,null=True, related_name=
                                  "departments",blank=True)
    address = models.CharField("Адрес", default=None, max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "Отдел"
        verbose_name_plural = "Отделы"

    def __str__(self):
        return self.title

class UserManager(BaseUserManager):
    def _create_user(self, fullname, email, password=None, **extra_fields):
        if not fullname:
            raise ValueError('Указанное имя пользователя должно быть установлено')

        if not email:
            raise ValueError('Данный адрес электронной почты должен быть установлен')

        email = self.normalize_email(email)
        user = self.model(fullname=fullname, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # if user.status == "Студент":
        #     user.departments.set([1, 2, 3, 4, 5, 6, 7, 8])

        return user

    def create_student(self, fullname, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('status', 'Студент')

        return self._create_user(fullname, email, password, **extra_fields)

    def create_staff(self, fullname, email, password=None, **extra_fields):
        # extra_fields.setdefault('is_student', False)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('status', 'Работник')
        extra_fields.setdefault('is_active', False)

        return self._create_user(fullname, email, password, **extra_fields)

    def create_superuser(self, fullname, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        #if extra_fields.get('is_staff') is not True:
        #    raise ValueError('Суперпользователь должен иметь is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self._create_user(fullname, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField(max_length=50)

    email = models.EmailField(
        validators=[validators.validate_email],
        unique=True,
        blank=False
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    STATUS = (
        ('Работник', 'работник'),
        ('Студент', 'студент'),
        ('Администратор', 'администратор'),
    )

    status = models.CharField(max_length=20, choices=STATUS, blank=True, help_text='Статус пользователя')
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ('fullname',)

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.fullname

class Staff(models.Model):
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE, primary_key=True, related_name="staff")
    department = models.ForeignKey(Department, verbose_name="Отдел", on_delete=models.SET_NULL, null=True, blank=True, related_name="department")
    contactNumber = models.CharField("Контактный номер", default="Номер не установлен", max_length=50)

    def __str__(self):
        return self.user.fullname

class Student(models.Model):
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE, primary_key=True, related_name="student")
    group = models.ForeignKey(Group, verbose_name="Группа", on_delete=models.SET_NULL, null=True, blank=True, related_name="group")

    def __str__(self):
        return self.user.fullname

class ModuleTemplate(models.Model):
    title = models.CharField("Название модуля", max_length=50)
    points = models.TextField("Список пунктов")

class Module(models.Model):
    title = models.CharField("Название модуля", default=None, max_length=50)
    student_id = models.ForeignKey(Student, verbose_name="Студент", on_delete=models.CASCADE, null=False)
    module_template = models.ForeignKey(ModuleTemplate, verbose_name="Шаблон", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Модуль"
        verbose_name_plural = "Модули"

    def __str__(self):
        return self.title

class Statement(models.Model):
    title = models.CharField("Название заявления", default=None, max_length=50)
    img = models.ImageField("Файл", upload_to="Kemsu_Document/media/statement_documents", blank=True)
    module = models.ForeignKey(Module, verbose_name="Обходной лист", on_delete=models.CASCADE, null=False, related_name="statements")

    STATUS = (
        ('На рассмотрении', 'На рассмотрении'),
        ('Одобренно', 'Одобренно'),
        ('Отказанно', 'Отказанно')
    )

    status = models.CharField(max_length=20, choices=STATUS, blank=True, default='На рассмотрении', help_text='Статус заявления')

    def __str__(self):
        return self.title

class Point(models.Model):
    title = models.CharField("Название пункта", default=None, max_length=50)
    description = models.TextField("Описание", default=None, blank=True)
    module_id = models.ForeignKey(Module, verbose_name="Модуль", on_delete=models.SET_NULL, null=True, blank=True, related_name="points")
    staff = models.ForeignKey(Staff, verbose_name="Работник", on_delete=models.SET_NULL, null=True, blank=True)

    STATUS = (
        ('Не отправленно', 'но'),
        ('На подписании', 'нп'),
        ('Отказанно', 'о'),
        ('Подписанно', 'п'),
    )
    status = models.CharField(max_length=20, choices=STATUS, blank=True, default='Не отправленно', help_text='Статус пункта')

    def create_module(self, name, description, module):
        self.name = name
        self.description = description
        self.module_id = module
        self.save()

    class Meta:
        verbose_name = "Пункт"
        verbose_name_plural = "Пункты"

    def __str__(self):
        return self.title

class UploadedDocuments(models.Model):
    title = models.CharField("Название документа", default=None, max_length=50)
    img = models.ImageField("Файл", upload_to="Kemsu_Document/media/uploaded_documents", blank=True)
    point = models.ForeignKey(Point, verbose_name="Пункт", on_delete=models.CASCADE, null=False, related_name="uploadedDocuments")

    def __str__(self):
        return self.title

class RequiredDocuments(models.Model):
    title = models.CharField("Название документа", default=None, max_length=50)
    img = models.ImageField("Файл", upload_to="Kemsu_Document/media/required_documents", blank=True)
    point = models.ForeignKey(Point, verbose_name="Пункт", on_delete=models.CASCADE, null=False, related_name="requiredDocuments")

    def __str__(self):
        return self.title

