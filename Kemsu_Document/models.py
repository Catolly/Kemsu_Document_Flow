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
    name = models.CharField("Название группы", default=None, max_length=50, unique=True)
    recruitment_date = models.DateField("Дата набора", default=date.today)
    institute = models.ForeignKey(Institute, verbose_name="Институт", on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.name

class Department(models.Model):
    title = models.CharField("Название отдела", default=None, max_length=100)
    institute = models.ForeignKey(Institute, verbose_name= "Институт", on_delete=models.CASCADE,null=True, related_name=
                                  "departments",blank=True)
    address = models.CharField("Адрес", default=None, max_length=100, null=True, blank=True)

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
    fullname = models.CharField(max_length=50)

    email = models.EmailField(
        validators=[validators.validate_email],
        # unique=True,
        blank=True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    STATUS = (
        ('Работник', 'работник'),
        ('Студент', 'студент'),
        ('Администратор', 'администратор'),
    )

    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('None', 'None')
    )

    gender = models.CharField(max_length=10, choices=GENDER, blank=True, default='None')
    status = models.CharField(max_length=20, choices=STATUS, blank=True, help_text='Статус пользователя')
    USERNAME_FIELD = 'id'
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
    RECRUITMENT_FORM = (
        ('Бюджет', 'Бюджет'),
        ('Коммерция', 'Коммерция'),
    )
    STATUS = (
        ('Учится', 'Учится'),
        ('В академ. отпуске', 'В академ. отпуске'),
    )

    EDUCATION_FORM = (
        ('Очная', 'Очная'),
        ('Очно-заочная', 'Очно-заочная'),
        ('Заочная', 'Заочная'),
    )

    educationForm = models.CharField("Форма обучения", max_length=20, choices=EDUCATION_FORM, blank=True,
                                     help_text="Форма обучения")

    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE, primary_key=True, related_name="student")
    group = models.ForeignKey(Group, verbose_name="Группа", on_delete=models.SET_NULL, null=True, blank=True, related_name="group")
    recruitmentForm = models.CharField(max_length=20, choices=RECRUITMENT_FORM, blank=True, help_text='Форма набора')
    status = models.CharField(max_length=20, choices=STATUS, default='Учится', blank=True, help_text='Статус')

    def __str__(self):
        return self.user.fullname

class BypassSheetTemplate(models.Model):
    name = models.CharField("Название модуля", default=None, max_length=50)
    studentList = models.ManyToManyField(Student, verbose_name="Студент", related_name="bypassSheetTemplate")

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
    title = models.CharField("Название заявления", default=None, max_length=50)
    bypass_sheet_template = models.ForeignKey(BypassSheetTemplate, verbose_name="Шаблон обходного листа", on_delete=models.CASCADE, null=False, related_name="statements")
    img = models.FileField("Шаблон заявления", upload_to="statement_documents/", blank=True)

    class Meta:
        verbose_name = "Шаблон заявления"
        verbose_name_plural = "Шаблоны заявлений"

    def __str__(self):
        return self.title

class PointTemplate(models.Model):
    title = models.CharField("Название пункта", default=None, max_length=50)
    description = models.TextField("Описание", default=None, blank=True)
    bypass_sheet_template = models.ForeignKey(BypassSheetTemplate, verbose_name="Шаблон обходного листа", on_delete=models.CASCADE, related_name="points")
    department = models.ForeignKey(Department, verbose_name="Отдел", on_delete=models.SET_NULL, null=True, related_name="points_template")

    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('None', 'None')
    )

    gender = models.CharField(max_length=10, choices=GENDER, blank=True, default='None')

    class Meta:
        verbose_name = "Шаблон пункта"
        verbose_name_plural = "Шаблоны пунктов"

    def __str__(self):
        return self.title

class BypassSheet(models.Model):
    name = models.CharField("Название модуля", default=None, max_length=50)
    student_id = models.ForeignKey(Student, verbose_name="Студент", on_delete=models.CASCADE, null=False, related_name='bypassSheet')
    # bypass_sheet_template = models.OneToOneField(BypassSheetTemplate, verbose_name="Шаблон обходного листа", on_delete=models.SET_NULL, null=True, related_name='BypassSheet')

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
    title = models.CharField("Название заявления", default=None, max_length=50)
    bypass_sheet = models.ForeignKey(BypassSheet, verbose_name="Обходной лист", on_delete=models.CASCADE, null=False, related_name="statements")
    file = models.FileField("Документ", upload_to="statement_documents/", blank=True)
    # statement_template = models.OneToOneField(StatementsTemplate, verbose_name="Шаблон заявления", on_delete=models.SET_NULL, null=True, related_name='statements')
    img = models.FileField("Шаблон заявления", upload_to="statement_documents/", blank=True)

    STATUS = (
        ('На рассмотрении', 'На рассмотрении'),
        ('Одобренно', 'Одобренно'),
        ('Отказанно', 'Отказанно')
    )

    status = models.CharField(max_length=20, choices=STATUS, blank=True, default='На рассмотрении', help_text='Статус заявления')

    class Meta:
        verbose_name = "Заявление"
        verbose_name_plural = "Заявления"

    def __str__(self):
        return self.title

class Point(models.Model):
    title = models.CharField("Название пункта", default=None, max_length=50)
    bypass_sheet = models.ForeignKey(BypassSheet, verbose_name="Модуль", on_delete=models.SET_NULL, null=True, blank=True, related_name="points")
    staff = models.ForeignKey(Staff, verbose_name="Работник", on_delete=models.SET_NULL, null=True, blank=True)
    rejectReason = models.TextField("Причина отказа", null=True, blank=True)
    # point_template = models.ForeignKey(PointTemplate, verbose_name="Шаблон модуля", on_delete=models.SET_NULL, null=True, related_name="points")
    description = models.TextField("Описание", default=None, blank=True)
    department = models.ForeignKey(Department, verbose_name="Отдел", on_delete=models.SET_NULL, null=True,
                                   related_name="points")

    STATUS = (
        ('Не отправленно', 'Не отпрвленно'),
        ('На подписании', 'На подписании'),
        ('Отказанно', 'Отказанно'),
        ('Подписанно', 'Подписанно'),
    )

    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('None', 'None')
    )

    status = models.CharField(max_length=20, choices=STATUS, blank=True, default='Не отправленно', help_text='Статус пункта')
    gender = models.CharField(max_length=10, choices=GENDER, blank=True, default='None')

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
    img = models.ImageField("Файл", upload_to="required_documents/", blank=True)
    point = models.ForeignKey(PointTemplate, verbose_name="Пункт", on_delete=models.CASCADE, null=False, related_name="requiredDocuments")

    def __str__(self):
        return self.title

class UploadDocumentsFormat(models.Model):
    title = models.CharField("Название документа", default=None, max_length=50)
    format = models.CharField("Название документа", default=None, max_length=100)
    filesCount = models.PositiveSmallIntegerField("Кол-во загружаемых документов")
    point_template = models.ForeignKey(PointTemplate, verbose_name="Шаблон пункта", on_delete=models.CASCADE, null=False, related_name='uploadDocumentsFormat')

    def __str__(self):
        return self.title