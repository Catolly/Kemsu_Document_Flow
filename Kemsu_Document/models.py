import os
from datetime import date

from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.dispatch import receiver


class Institute(models.Model):
    title = models.CharField("Название института", default=None, max_length=100)

    class Meta:
        verbose_name = "Институт"
        verbose_name_plural = "Институты"

    def __str__(self):
        return self.title

class Group(models.Model):
    name = models.CharField("Название группы", default=None, max_length=15)
    course = models.SmallIntegerField(default=1)
    institute = models.ForeignKey(Institute, verbose_name="Институт", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.name

class Department(models.Model):
    title = models.CharField("Название отдела", default=None, max_length=150)
    institute = models.ForeignKey(Institute, verbose_name= "Институт", on_delete=models.CASCADE,null=True, related_name=
                                  "departments",blank=True)
    address = models.CharField("Адрес", default=None, max_length=150, null=True, blank=True)

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
    fullname = models.CharField(max_length=100)

    email = models.EmailField(
        validators=[validators.validate_email],
        # unique=True,
        blank=True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_baned = models.BooleanField(default=False)

    STATUS = (
        ('Работник', 'работник'),
        ('Студент', 'студент'),
        ('Администратор', 'администратор'),
    )

    GENDER = (
        ('Жен', 'Жен'),
        ('Муж', 'Муж'),
        ('None', 'None')
    )

    gender = models.CharField(max_length=10, choices=GENDER, blank=True, default='None')
    status = models.CharField(max_length=20, choices=STATUS, blank=True, help_text='Статус пользователя')
    USERNAME_FIELD = 'id'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ('fullname', 'email')



    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.fullname + ' - ' + self.email

class Staff(models.Model):
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE, primary_key=True, related_name="staff")
    department = models.ForeignKey(Department, verbose_name="Отдел", on_delete=models.SET_NULL, null=True, blank=True, related_name="staff")

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return self.user.fullname

class Student(models.Model):
    STATUS = (
        ('Учащийся', 'Учащийся'),
        ('Закончил', 'Закончил'),
    )

    EDUCATION_FORM = (
        ('Очная', 'Очная'),
        ('Очно-заочная', 'Очно-заочная'),
        ('Заочная', 'Заочная'),
    )

    educationForm = models.CharField("Форма обучения", max_length=20, choices=EDUCATION_FORM, blank=True,
                                     help_text="Форма обучения")
    year_of_admission = models.CharField(max_length=15, null=True)
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE, primary_key=True, related_name="student")
    group = models.ForeignKey(Group, verbose_name="Группа", on_delete=models.SET_NULL, null=True, blank=True, related_name="group")
    recruitmentForm = models.CharField(max_length=50, blank=True, help_text='Форма набора')
    status = models.CharField(max_length=20, choices=STATUS, default='Учащийся', blank=True, help_text='Статус')
    degree_of_study = models.CharField(max_length=30, blank=True, help_text='Степень обучения')

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"

    def __str__(self):
        return self.user.fullname

class BypassSheetTemplate(models.Model):
    title = models.CharField("Название модуля", default=None, max_length=100)
    studentList = models.ManyToManyField(Student, verbose_name="Студент", related_name="bypassSheetTemplate", null=True, max_length=10000, blank=True)

    EDUCATION_FORM = (
        ('Очная', 'Очная'),
        ('Очно-заочная', 'Очно-заочная'),
        ('Заочная', 'Заочная'),
    )

    educationForm = models.CharField("Форма обучения", max_length=20, choices=EDUCATION_FORM, blank=True, help_text="Форма обучения")

    class Meta:
        verbose_name = "Шаблон обходного листа"
        verbose_name_plural = "Шаблоны обходных листов"

    def __str__(self):
        return self.title

class StatementsTemplate(models.Model):
    bypass_sheet_template = models.ForeignKey(BypassSheetTemplate, verbose_name="Шаблон обходного листа", on_delete=models.CASCADE, null=True, related_name="statements")
    img = models.FileField("Шаблон заявления", upload_to="statement_documents/", blank=True, max_length=1000)

    class Meta:
        verbose_name = "Шаблон заявления"
        verbose_name_plural = "Шаблоны заявлений"

    def __str__(self):
        return self.bypass_sheet_template.title

    def delete(self, *args, **kwargs):
        storage, path = self.img.storage, self.img.path

        super(StatementsTemplate, self).delete(*args, **kwargs)
        storage.delete(path)

class PointTemplate(models.Model):
    title = models.CharField("Название пункта", default=None, max_length=100)
    description = models.TextField("Описание", default=None, blank=True, null=True)
    bypass_sheet_template = models.ForeignKey(BypassSheetTemplate, verbose_name="Шаблон обходного листа", on_delete=models.CASCADE, related_name="points")
    department = models.ForeignKey(Department, verbose_name="Отдел", on_delete=models.CASCADE, null=True, related_name="points_template")
    commonReasons = models.TextField(null=True, blank=True)

    GENDER = (
        ('Муж', 'Муж'),
        ('Жен', 'Жен'),
        ('None', 'None')
    )

    gender = models.CharField(max_length=10, choices=GENDER, blank=True, default='None')

    class Meta:
        verbose_name = "Шаблон пункта"
        verbose_name_plural = "Шаблоны пунктов"

    def __str__(self):
        return self.title

class BypassSheet(models.Model):
    title = models.CharField("Название модуля", default=None, max_length=100)
    student_id = models.ForeignKey(Student, verbose_name="Студент", on_delete=models.CASCADE, null=False, related_name='bypassSheets')
    bypass_sheet_template = models.ForeignKey(BypassSheetTemplate, verbose_name="Шаблон обходного листа", on_delete=models.CASCADE, null=True, related_name='BypassSheet')

    STATUS = (
        ('Подписан', 'Подписан'),
        ('Не подписан', 'Не подписан')
    )

    EDUCATION_FORM = (
        ('Очная', 'Очная'),
        ('Очно-заочная', 'Очно-заочная'),
        ('Заочная', 'Заочная'),
    )

    educationForm = models.CharField("Форма обучения", max_length=20, choices=EDUCATION_FORM, blank=True,
                                     help_text="Форма обучения")

    status = models.CharField("Подпись", max_length=20, choices=STATUS, default='Не подписан',
                              help_text="Форма обучения")
    class Meta:
        verbose_name = "Обходной лист"
        verbose_name_plural = "Обходные листы"

    def __str__(self):
        return self.title

class Statement(models.Model):
    bypass_sheet = models.ForeignKey(BypassSheet, verbose_name="Обходной лист", on_delete=models.CASCADE, null=True, related_name="statements")
    file = models.FileField("Документ", upload_to="statement_documents/", blank=True, max_length=1000)
    # statement_template = models.ForeignKey(StatementsTemplate, verbose_name="Шаблон заявления", on_delete=models.CASCADE, null=True, related_name='statements')

    STATUS = (
        ('На рассмотрении', 'На рассмотрении'),
        ('Одобрено', 'Одобрено'),
        ('Отказано', 'Отказано')
    )

    status = models.CharField(max_length=20, choices=STATUS, blank=True, default='На рассмотрении', help_text='Статус заявления')

    class Meta:
        verbose_name = "Заявление"
        verbose_name_plural = "Заявления"

    def __str__(self):
        return self.bypass_sheet.title

    def delete(self, *args, **kwargs):
        storage, path = self.file.storage, self.file.path

        super(Statement, self).delete(*args, **kwargs)
        storage.delete(path)

class Point(models.Model):
    title = models.CharField("Название пункта", default=None, max_length=100)
    bypass_sheet = models.ForeignKey(BypassSheet, verbose_name="Модуль", on_delete=models.CASCADE, null=True, blank=True, related_name="points")
    staff = models.ForeignKey(Staff, verbose_name="Работник", on_delete=models.SET_NULL, null=True, blank=True)
    rejectReason = models.TextField("Причина отказа", null=True, blank=True)
    point_template = models.ForeignKey(PointTemplate, verbose_name="Шаблон модуля", on_delete=models.CASCADE, null=True, related_name="points")
    description = models.TextField("Описание", default=None, blank=True, null=True)
    department = models.ForeignKey(Department, verbose_name="Отдел", on_delete=models.CASCADE, null=True,
                                   related_name="points")

    STATUS = (
        ('Не отправлено', 'Не отправлено'),
        ('На подписании', 'На подписании'),
        ('Отказано', 'Отказано'),
        ('Подписано', 'Подписано'),
    )

    GENDER = (
        ('Муж', 'Муж'),
        ('Жен', 'Жен'),
        ('None', 'None')
    )

    status = models.CharField(max_length=20, choices=STATUS, blank=True, default='Не отправлено', help_text='Статус пункта')
    gender = models.CharField(max_length=10, choices=GENDER, blank=True, default='None')

    class Meta:
        verbose_name = "Пункт"
        verbose_name_plural = "Пункты"

    def __str__(self):
        return self.title

class UploadedDocuments(models.Model):
    img = models.FileField("Файл", upload_to="uploaded_documents/", blank=True, max_length=1000)
    point = models.ForeignKey(Point, verbose_name="Пункт", on_delete=models.CASCADE, null=True, related_name="uploadedDocuments")

    class Meta:
        verbose_name = "Загруженный документ"
        verbose_name_plural = "Загруженные документы"

    def __str__(self):
        return self.point.title

    # def delete(self, *args, **kwargs):
    def delete(self, using=None, keep_parents=False):
        print("=====delete=====")
        storage, path = self.img.storage, self.img.path

        super(UploadedDocuments, self).delete(using, keep_parents)
        storage.delete(path)

class RequiredDocumentsTemplate(models.Model):
    img = models.FileField("Файл", upload_to="required_documents/", blank=True, max_length=1000)
    point_template = models.ForeignKey(PointTemplate, verbose_name="Шаблон пункта", on_delete=models.CASCADE,
                                       null=True, related_name="requiredDocuments")

    class Meta:
        verbose_name = "Шаблон требуемых документов"
        verbose_name_plural = "Шаблоны требуемых документов"

    def __str__(self):
        return self.point_template.title

    def delete(self, *args, **kwargs):
        storage, path = self.img.storage, self.img.path

        super(RequiredDocumentsTemplate, self).delete(*args, **kwargs)
        storage.delete(path)

class RequiredDocuments(models.Model):
    img = models.FileField("Файл", upload_to="required_documents/", blank=True, max_length=1000)
    point = models.ForeignKey(Point, verbose_name="Пункт", on_delete=models.CASCADE,
                                       null=True, related_name="requiredDocuments")
    requiredDocumentsTemplate = models.ForeignKey(RequiredDocumentsTemplate, verbose_name='Шаблон', on_delete=models.CASCADE, null=True, related_name="requiredDocuments")

    class Meta:
        verbose_name = "Требуемый документ"
        verbose_name_plural = "Требуемые документы"

    def __str__(self):
        return self.point.title

    # def delete(self, *args, **kwargs):
    def delete(self, using=None, keep_parents=False):
        print("=====delete=====")

        storage, path = self.img.storage, self.img.path

        super(RequiredDocuments, self).delete(using, keep_parents)
        storage.delete(path)

class UploadDocumentsFormat(models.Model):
    title = models.CharField("Формат", default=None, max_length=100)
    point_template = models.ForeignKey(PointTemplate, verbose_name="Шаблон пункта", on_delete=models.CASCADE, null=True, related_name='uploadDocumentsFormat')

    class Meta:
        verbose_name = "Формат загруженого документы"
        verbose_name_plural = "Форматы загруженных документов"

    def __str__(self):
        return self.title

class Deadline(models.Model):
    groupName = models.ForeignKey(Group, verbose_name='Группа', on_delete=models.CASCADE, related_name='deadlines')
    deadline = models.CharField(max_length=20)
    bypass_sheets_template = models.ForeignKey(BypassSheetTemplate, verbose_name='Обходной лист', on_delete=models.CASCADE, related_name='deadlines')

    class Meta:
        verbose_name = 'Крайний срок подписания документов'
        verbose_name_plural = 'Крайние сроки подписания документов'

    def __str__(self):
        return self.groupName.name + ' - ' + self.bypass_sheets_template.title