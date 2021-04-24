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

# class Student(models.Model):
#     date_of_enrollment = models.DateField("Дата зачисления", default=date.today)
#     group_id = models.ForeignKey(Group, verbose_name="Группа", on_delete=models.CASCADE, null=False)
#     #module_id = models.ManyToManyField(Module, verbose_name="Модули", related_name="student_module", blank=True)
#
#     first_name = models.CharField(max_length=50, default=None, null=True, blank=True)
#     last_name = models.CharField(max_length=50, default=None, null=True, blank=True)
#     patronymic = models.CharField(max_length=50, default=None, null=True, blank=True)
#
#     class Meta:
#         verbose_name = "Студент"
#         verbose_name_plural = "Студенты"
#
#     def __str__(self):
#         return "Студент"

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

# class Staff(models.Model):
#
#     department_id = models.ForeignKey(Department, verbose_name="Отдел", on_delete=models.SET_NULL, null=True)
#
#     first_name = models.CharField(max_length=50, default=None, null=True, blank=True)
#     last_name = models.CharField(max_length=50, default=None, null=True, blank=True)
#     patronymic = models.CharField(max_length=50, default=None, null=True, blank=True)
#
#     class Meta:
#         verbose_name = "Работник"
#         verbose_name_plural = "Работники"
#
#     def __str__(self):
#         return str(self.department_id)


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
        # extra_fields.setdefault('is_student', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('status', 'Студент')
        #extra_fields.setdefault('institute', extra_fields.get('group').institute_id)

        return self._create_user(fullname, email, password, **extra_fields)

    def create_staff(self, fullname, email, password=None, **extra_fields):
        # extra_fields.setdefault('is_student', False)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('status', 'Работник')

        return self._create_user(fullname, email, password, **extra_fields)

    def create_superuser(self, fullname, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        #extra_fields.setdefault('is_student', False)

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
    #is_student = models.BooleanField(default=False)

    #department = models.ForeignKey(Department, verbose_name="Отдел", on_delete=models.SET_NULL, null=True, blank=True)
    #group = models.ForeignKey(Group, verbose_name="Группа", on_delete=models.SET_NULL, null=True, blank=True)
    #departments = models.ManyToManyField(Department, verbose_name="Отделы", related_name="student_departments")
    #institute = models.ForeignKey(Institute, verbose_name="Институт", on_delete=models.SET_NULL, null=True, blank=True)

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
    recordBookNumber = models.CharField("Номер зачётной книжки", max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.fullname

class Module(models.Model):
    title = models.CharField("Название модуля", default=None, max_length=50)
    student_id = models.ForeignKey(User, verbose_name="Студент", on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "Модуль"
        verbose_name_plural = "Модули"

    def __str__(self):
        return self.title

class Statement(models.Model):
    title = models.CharField("Название заявления", default=None, max_length=50)
    img = models.ImageField("Изображение", upload_to="Kemsu_Document/media/statement_images", blank=True)
    module = models.ForeignKey(Module, verbose_name="Обходной лист", on_delete=models.CASCADE, null=False, related_name="statements")
    file = models.FileField("Документ", upload_to="media/",blank=True )
    def __str__(self):
        return self.title


class Point(models.Model):
    #title = models.ForeignKey(Department, verbose_name='Название пункта', on_delete=models.CASCADE, null=False)
    title = models.CharField("Название пункта", default=None, max_length=50)
    description = models.TextField("Описание", default=None, blank=True)
    #file = models.ImageField("Файл", upload_to="Kemsu_Document/media/", blank=True)
    module_id = models.ForeignKey(Module, verbose_name="Модуль", on_delete=models.SET_NULL, null=True, blank=True, related_name="points")
    staff = models.ForeignKey(Staff, verbose_name="Работник", on_delete=models.SET_NULL, null=True, blank=True)
    #point_id = models.ForeignKey(Department, verbose_name="Отдел", on_delete=models.SET_NULL, null=True, blank=True)

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

