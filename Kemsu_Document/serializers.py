from collections import OrderedDict
from datetime import time, datetime
import json

import jwt
from django.core.mail import send_mail
from psycopg2.compat import text_type
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from djangoProject import settings
from django.utils.text import gettext_lazy as _
import time

from .exceptions import GroupNotFoundError, ThisUserIsAlreadyExistException, ThisEmailIsAlreadyExistError, \
    DepartmentNotFoundException, UserWithThisFullNameDoesNotExistException, UserWithThisEmailDoesNotExistException, \
    BypassSheetTemplateExistException
from .models import (
    User, Department, Group, Institute,
    BypassSheet, Point, Statement, UploadedDocuments, RequiredDocuments, Staff, Student, BypassSheetTemplate,
    StatementsTemplate, PointTemplate, UploadDocumentsFormat, RequiredDocumentsTemplate, Deadline,
)

class RegistrationStaffSerializer(serializers.ModelSerializer):

    department = serializers.CharField(max_length=150, write_only=True)
    fullname = serializers.CharField(max_length=150, write_only=True)
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )
    email = serializers.EmailField(max_length=150, write_only=True)

    class Meta:
        model = Staff
        fields = ('fullname', 'password', 'email', 'department')

    def create(self, validated_data):
        user_data = dict()

        user_email = User.objects.filter(email=validated_data['email']).first()
        if user_email:
            raise ThisEmailIsAlreadyExistError

        user_data.setdefault('fullname', validated_data.pop('fullname'))
        user_data.setdefault('email', validated_data.pop('email'))
        user_data.setdefault('password', validated_data.pop('password'))

        try:
            department = Department.objects.get(title=validated_data['department'])
        except Exception:
            raise DepartmentNotFoundException
        try:
            if department.title == 'Отдел администрирования':
                user_data['status'] = 'Администратор'
            user = User.objects.create_staff(**user_data)
        except Exception:
            raise ThisEmailIsAlreadyExistError

        validated_data['user'] = user

        validated_data['department'] = department

        Staff.objects.create(**validated_data)

        return user


class RegistrationStudentSerializer(serializers.ModelSerializer):

    group = serializers.CharField(max_length=150, write_only=True)
    fullname = serializers.CharField(max_length=150, write_only=True)
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )
    email = serializers.EmailField(max_length=150, write_only=True)

    tokens = serializers.SerializerMethodField(read_only=True)

    id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Student
        fields = ('id', 'fullname', 'group', 'email', 'password', 'tokens')

    def get_id(self, user):
        return user.id

    def get_tokens(self, user):
        tokens = RefreshToken.for_user(user)
        refresh = text_type(tokens)
        access = text_type(tokens.access_token)
        data = {
            "refresh": refresh,
            "access": access,
            "expiresIn" : int(round(time.time() * 1000)) + int(round(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].seconds * 1000))
        }
        return data

    def validate(self, attrs):
        self.PASSWORD = attrs.pop('password')
        return attrs

    def create(self, validated_data):

        user = Student.objects.get(group__name=validated_data['group'], user__fullname=validated_data['fullname']).user

        # for student in student_data:
        #     user = User.objects.filter(fullname=validated_data['fullname'], id=student.user.id).first()
        #     if user:
        #         break

        user_email = User.objects.filter(email=validated_data['email']).first()
        if user_email:
            raise ThisEmailIsAlreadyExistError

        user.set_password(self.PASSWORD)
        user.email = validated_data['email']
        user.is_active = True

        user.save()

        return user

class GroupSerializer(serializers.ModelSerializer):

    institute = serializers.SlugRelatedField(slug_field='title', read_only=True)
    courseNumber = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Group
        fields = ('name', 'institute', 'courseNumber')

    def get_courseNumber(self, group):

        return group.course

class InstituteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Institute
        fields = "__all__"

class ModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = BypassSheet
        fields = "__all__"

class UploadedDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadedDocuments
        fields = ("img",)

class RequiredDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequiredDocuments
        fields = ("img",)

class StaffSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    fullname = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField(read_only=True)
    department = serializers.SlugRelatedField(slug_field='title', read_only=True)
    isBaned = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Staff
        fields = ('id', 'fullname', 'email', 'department', 'isBaned')

    def get_isBaned(self, staff):
        return staff.user.is_baned

    def get_id(self, staff):
        return staff.user.id

    def get_fullname(self, staff):
        return staff.user.fullname

    def get_email(self, staff):
        return staff.user.email

    @classmethod
    def setup_eager_loading(cls, queryset):

        # queryset = queryset.select_related('user')

        return queryset

class PointSerializer(serializers.ModelSerializer):

    uploadedDocuments = serializers.SerializerMethodField()
    staff = serializers.SerializerMethodField()
    requiredDocuments = serializers.SerializerMethodField()
    uploadDocumentsFormat = serializers.SerializerMethodField()
    commonReasons = serializers.SerializerMethodField()
    bypassSheetId = serializers.SerializerMethodField()
    deadline = serializers.SerializerMethodField()

    class Meta:
        model = Point
        fields = ("bypassSheetId", "title", "status", "uploadedDocuments", "staff", "rejectReason", 'requiredDocuments', 'uploadDocumentsFormat', 'commonReasons',
                  'description', 'deadline')

    def get_deadline(self, point):

        bypass_sheet = point.bypass_sheet

        bypass_sheet_template = bypass_sheet.bypass_sheet_template

        group = bypass_sheet.student_id.group

        deadline = Deadline.objects.filter(bypass_sheets_template=bypass_sheet_template, groupName=group).first()

        if deadline is None:
            return ''
        return deadline.deadline

    def get_uploadedDocuments(self, point):
        uploaded_documents = UploadedDocuments.objects.filter(point=point)

        files = []

        for uploaded_document in uploaded_documents:
            files.append(uploaded_document.img.url)

        return files

    def get_requiredDocuments(self, point):
        required_documents = RequiredDocuments.objects.filter(point=point)

        files = []

        for required_document in required_documents:
            files.append(required_document.img.url)

        return files

    def get_staff(self, point):
        try:
            return point.staff.user.fullname
        except AttributeError:
            return ""

    def get_bypassSheetId(self, point):
        return point.bypass_sheet.id

    def get_commonReasons(self, point):
        point_template = point.point_template

        common_reasons_in_string = point_template.commonReasons

        if common_reasons_in_string == "" or common_reasons_in_string == None:
            return []

        common_reasons_in_list = common_reasons_in_string.split('<separator>')

        common_reasons_in_list.pop()

        return common_reasons_in_list

    def get_uploadDocumentsFormat(self, point):
        point_template = point.point_template

        upload_documents_format = UploadDocumentsFormat.objects.filter(point_template=point_template)

        titles = []

        for upload_document_format in upload_documents_format:
            titles.append({'title': upload_document_format.title})

        return titles


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'fullname', 'email')

class StatementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Statement
        fields = ("file", )

class BypassSheetsSerializer(serializers.ModelSerializer):

    statements = serializers.SerializerMethodField(read_only=True)
    points = PointSerializer(many=True, read_only=True)
    deadline = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BypassSheet
        fields = ("id", "title", "statements", "points", "status", "deadline")

    def get_deadline(self, bypass_sheet):
        deadline = Deadline.objects.filter(groupName=bypass_sheet.student_id.group, bypass_sheets_template=bypass_sheet.bypass_sheet_template).first()

        if deadline is None:
            return ''
        return deadline.deadline

    def get_statements(self, bypass_sheet):
        statements = Statement.objects.filter(bypass_sheet=bypass_sheet)

        files = []

        for statement in statements:
            files.append(statement.file.url)

        return files

    @classmethod
    def setup_eager_loading(cls, queryset):

        queryset = queryset.prefetch_related('points', 'statements')

        return queryset

class StudentSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField(read_only=True)
    fullname = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField(read_only=True)
    group = serializers.SlugRelatedField(slug_field='name', read_only=True)
    institute = serializers.SerializerMethodField(read_only=True)
    courseNumber = serializers.SerializerMethodField(read_only=True)
    bypassSheets = BypassSheetsSerializer(read_only=True, many=True)
    isBaned = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Student
        fields = ('id', 'fullname', 'email', 'recruitmentForm', 'status', 'group',
                  'institute', 'courseNumber', 'bypassSheets', 'isBaned', 'educationForm')

    def get_isBaned(self, student):
        return student.user.is_baned

    def get_id(self, student):
        return student.user.id

    def get_fullname(self, student):
        return student.user.fullname

    def get_email(self, student):
        return student.user.email

    def get_institute(self, student):

        return student.group.institute.title

    def get_courseNumber(self, student):

        return student.group.course

    @classmethod
    def setup_eager_loading(cls, queryset):
        queryset = queryset.select_related('user')

        queryset = queryset.prefetch_related('group', 'bypassSheets')

        return queryset

class StudentTestSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField(read_only=True)
    fullname = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField(read_only=True)
    group = serializers.SlugRelatedField(slug_field='name', read_only=True)
    institute = serializers.SerializerMethodField(read_only=True)
    courseNumber = serializers.SerializerMethodField(read_only=True)
    bypassSheets = BypassSheetsSerializer(read_only=True, many=True)
    # bypassSheets = serializers.SerializerMethodField(read_only=True)
    isBaned = serializers.SerializerMethodField(read_only=True)
    recruitmentForm = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    educationForm = serializers.SerializerMethodField(read_only=True)

    def get_educationForm(self, student):
        return student.educationForm

    def get_status(self, student):
        return student.status

    def get_recruitmentForm(self, student):
        return student.recruitmentForm

    def get_isBaned(self, student):
        return student.user.is_baned

    def get_id(self, student):
        return student.user.id

    def get_fullname(self, student):
        return student.user.fullname

    def get_email(self, student):

        return student.user.email

    def get_institute(self, student):
        return student.group.institute.title

    def get_courseNumber(self, student):
        return student.group.course

    def get_bypassSheets(self, student):

        bypass_sheets_query = BypassSheet.objects.filter(student_id=student)

        sel_query = BypassSheetsSerializer().setup_eager_loading(bypass_sheets_query)

        serializers = BypassSheetsSerializer(sel_query, read_only=True, many=True)

        return serializers.data

    @classmethod
    def setup_eager_loading(cls, queryset):

        queryset = queryset.select_related('user')

        queryset = queryset.prefetch_related('group', 'bypassSheets')

        return queryset

class PostStatementsSerializer(serializers.ModelSerializer):

    file = serializers.ListField()

    class Meta:
        model = Statement
        fields = ('file',)

class PostByPassSheetsSerializer(serializers.ModelSerializer):

    statements = serializers.ListField()

    title = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        model = BypassSheet
        fields = ('title', 'statements')

    def statementsCreate(self, statements_data, module):

        statement_data = dict()

        for file in statements_data:
            statement_data['bypass_sheet'] = module
            statement_data['file'] = file
            Statement.objects.create(**statement_data)
            statement_data = dict()

    def __createRequiredDocuments(self, required_documents_template, point):

        required_documents_data = dict()

        for required_document_template in required_documents_template:
            required_documents_data['img'] = required_document_template.img
            required_documents_data['point'] = point
            required_documents_data['requiredDocumentsTemplate'] = required_document_template

            RequiredDocuments.objects.create(**required_documents_data)


    def __createPoints(self, bypass_sheet, student):
        bypass_sheet_template = BypassSheetTemplate.objects.get(title=bypass_sheet.title, educationForm=student.educationForm)

        bypass_sheet_template.studentList.add(student.user.id)

        points_template = PointTemplate.objects.filter(bypass_sheet_template = bypass_sheet_template)

        point_data = dict()

        for point_template in points_template:
            if ((student.user.gender != point.gender and point.gender != 'None') or (point.department.institute is not None and student.group.institute != point.department.institute)):
                continue

            point_data['title'] = point_template.title
            point_data['description'] = point_template.description
            point_data['gender'] = point_template.gender
            point_data['department'] = point_template.department
            point_data['bypass_sheet'] = bypass_sheet
            point_data['point_template'] = point_template

            point = Point.objects.create(**point_data)

            point_data = dict()

            required_documents_template = RequiredDocumentsTemplate.objects.filter(point_template=point_template)

            self.__createRequiredDocuments(required_documents_template, point)

    def create(self, validated_data):
        user = None
        request = self.context.get("request")

        if request and hasattr(request, "user"):
            user = request.user

        statements_data_ordered_dict = validated_data.pop('statements')

        statements_data = []

        for statement_data in statements_data_ordered_dict:
            statements_data.append(statement_data)

        student = Student.objects.get(user=user.id)

        bypass_sheet_template = BypassSheetTemplate.objects.get(title=validated_data['title'],
                                                                educationForm=student.educationForm)

        validated_data['student_id'] = student
        validated_data['educationForm'] = student.educationForm
        validated_data['bypass_sheet_template'] = bypass_sheet_template

        bypass_sheet = BypassSheet.objects.create(**validated_data)

        self.statementsCreate(statements_data, bypass_sheet)

        self.__createPoints(bypass_sheet, student)

        return bypass_sheet

class TokenEmailSerializer(Serializer):
    email = User.EMAIL_FIELD

    def __init__(self, *args, **kwargs):
        super(TokenEmailSerializer, self).__init__(*args, **kwargs)

        self.fields['email'] = serializers.CharField()
        self.fields['password'] = serializers.CharField(max_length=128, write_only=True)

    def getUser(self, attrs):
        return User.objects.filter(email=attrs['email']).first()


    def validate(self, attrs):
        self.user = self.getUser(attrs)

        if not self.user:
            raise ValidationError('Аккаунта с таким email не существует')

        if self.user:
            if not self.user.check_password(attrs['password']):
                raise ValidationError('Введен неверный пароль.')

        if self.user is None:
            raise ValidationError('No active account found with the given credentials')
        if not self.user.is_active:
            raise ValidationError('Your account has not been verified by the administrator')
        if self.user.is_baned:
            raise ValidationError('Your was baned in this system')

        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplemented(
            'Must implement `get_token` method for `MyTokenObtainSerializer` subclasses')


class TokenEmailPairSerializer(TokenEmailSerializer):

    @classmethod
    def get_tokens(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super(TokenEmailPairSerializer, self).validate(attrs)

        refresh = self.get_tokens(self.user)

        data['tokens'] = dict()
        data['tokens'].setdefault('refresh', text_type(refresh))
        data['tokens'].setdefault('access', text_type(refresh.access_token))
        data['tokens'].setdefault('expiresIn', int(round(time.time() * 1000)) + int(round(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].seconds * 1000)))
        data['fullname'] = self.user.fullname
        data['email'] = self.user.email
        data['gender'] = self.user.gender
        data['id'] = self.user.id

        if self.user.status == "Студент":
            student = Student.objects.filter(user=self.user).first()
            data['group'] = student.group.name
        else:
            staff = Staff.objects.filter(user=self.user).first()
            data['department'] = staff.department.title
        return data

class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('fullname',)

    def create(self, validated_data):
        user = User.objects.update_or_create(
            defaults = {
                'fullname' : validated_data.get('fullname')
            }
        )
        return user
class UpdateStatementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Statement
        fields = ('file', )

class SigningPointSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    status = serializers.CharField(write_only=True, required=False)
    rejectReason = serializers.CharField(required=False, write_only=True)
    requiredDocuments = serializers.ListField(write_only=True, allow_empty=True, required=False)

    class Meta:
        model = BypassSheet
        fields = ('id', 'status', 'rejectReason', 'requiredDocuments')

    def __updateRequiredDocuments(self, data, point):

        for file in data:

            if isinstance(file, str):
                file_arr = file.split('/')

                file = file_arr[-2]+'/'+file_arr[-1]

            obj, statement = RequiredDocuments.objects.update_or_create(img=file,
                                                                        point=point,
                                                                        defaults={
                                                                            'img': file
                                                                        })

    def __checkSigningPoints(self, bypass_sheet):

        points = Point.objects.filter(bypass_sheet=bypass_sheet)

        for point in points:
            if point.status != 'Подписано':
                return False
        return True

    def __updatePoint(self, data):

        bypass_sheet = BypassSheet.objects.filter(id=data['id']).first()

        point = Point.objects.filter(bypass_sheet=bypass_sheet, title=self.department_name).first()

        point.status = data.get('status', point.status)

        point.rejectReason = data.get('rejectReason', point.rejectReason)

        point.staff = Staff.objects.get(user=self.user)

        point.save()

        if point.rejectReason == "Отказано":
            student = bypass_sheet.student_id

            user = student.user

            send_mail('MyDoc', 'Вам было отказанно в подписании. Пожалуйста, проверьте ваш личный кабинет', 'mydockemsu@gmail.com', [user.email])

        try:
            self.__updateRequiredDocuments(data['requiredDocuments'], point)
        except KeyError:
            self.__updateRequiredDocuments([], point)

        if self.__checkSigningPoints(bypass_sheet):
            bypass_sheet.status = 'Подписан'
            bypass_sheet.save()
            student = bypass_sheet.student_id

            user = student.user

            send_mail('MyDoc', 'Ваш обходной лист был успешно подписан', 'mydockemsu@gmail.com', [user.email])

        else:
            bypass_sheet.status = 'Не подписан'
            bypass_sheet.save()

    def create(self, validated_data):

        self.department_name = self.context['department_name']
        self.user = self.context['user']

        self.__updatePoint(validated_data)

        return 1

class BypassSheetTemplateTitleSerializer(serializers.ModelSerializer):

    statements = serializers.SerializerMethodField()

    class Meta:
        model = BypassSheetTemplate
        fields = ('id', 'title', 'statements')

    def get_statements(self, bypass_sheet_template):
        statements_template = StatementsTemplate.objects.filter(bypass_sheet_template=bypass_sheet_template)

        statement_list = []

        for statement in statements_template:
            statement_list.append(statement.img.url)

        return statement_list

class PostUploadDocumentsFormatSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadDocumentsFormat
        fields = ('title',)

    def validate(self, attrs):
        return attrs

class PostPointTemplateSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    requiredDocuments = serializers.ListField(write_only=True, allow_empty=True, required=False)
    uploadDocumentsFormat = serializers.ListField(required=False,
                                                  child=PostUploadDocumentsFormatSerializer(write_only=True))
    commonReasons = serializers.ListField(write_only=True, allow_empty=True, required=False)

    class Meta:
        model = PointTemplate
        fields = ('id', 'title', 'description', 'requiredDocuments', 'gender', 'uploadDocumentsFormat', 'commonReasons')

    def validate(self, attrs):
        return attrs

class UpdateBypassSheetTemplateSerializer(serializers.ModelSerializer):
    statements = serializers.ListField(write_only=True, allow_empty=True, required=False)

    points = serializers.ListField(child=PostPointTemplateSerializer(write_only=True))

    studentList = serializers.ListField(write_only=True, allow_empty=True, allow_null=True, required=False)

    class Meta:
        model = BypassSheetTemplate
        fields = ('title', 'educationForm', 'statements', 'points', 'studentList')

    def update_statements_template(self, bypass_sheet_template, data):

        try:
            statements_template = data.pop('statements')
        except KeyError:
            statements_template = []
        statements_data = []

        for statement_data in statements_template:
            statements_data.append(statement_data)

        statement_template_data = dict()

        StatementsTemplate.objects.filter(bypass_sheet_template=bypass_sheet_template).delete()

        for file in statements_data:

            if isinstance(file, str):
                file_arr = file.split('/')

                file = file_arr[-2]+'/'+file_arr[-1]

            statement_template_data['img'] = file
            statement_template_data['bypass_sheet_template'] = bypass_sheet_template
            StatementsTemplate.objects.create(**statement_template_data)
            statement_template_data = dict()

    def update_required_documents_template(self, point_template, point_data):
        RequiredDocumentsTemplate.objects.filter(point_template=point_template).delete()

        try:
            required_documents = point_data.pop('requiredDocuments')
        except KeyError:
            required_documents = []

        required_documents_data = dict()

        files = []

        for statement_data in required_documents:
            files.append(statement_data)

        for file in files:

            if isinstance(file, str):
                file_arr = file.split('/')

                file = file_arr[-2]+'/'+file_arr[-1]

            required_documents_data['point_template'] = point_template
            required_documents_data['img'] = file

            RequiredDocumentsTemplate.objects.create(**required_documents_data)

            required_documents_data = dict()

    def update_upload_documents_format(self, point_template, point_data):

        UploadDocumentsFormat.objects.filter(point_template=point_template).delete()

        try:
            upload_documents_format = point_data.pop('uploadDocumentsFormat')
        except KeyError:
            upload_documents_format = []

        for upload_document_format in upload_documents_format:

            UploadDocumentsFormat.objects.update_or_create(title=dict(upload_document_format)['title'], point_template=point_template,
                                                           defaults={
                                                               'title': dict(upload_document_format)['title'],
                                                               'point_template': point_template
                                                           })

    def update_common_reasons(self, point_template, common_reasons):
        common_reasons_in_string = ""

        for common_reason in common_reasons:
            common_reasons_in_string += common_reason + "<separator>"

        point_template.commonReasons = common_reasons_in_string

        point_template.save()

    def delete_points_template(self, old_ids, bypass_sheet_template, points_template):

        # old_points_template = PointTemplate.objects.filter(bypass_sheet_template=bypass_sheet_template)

        new_ids = []

        for point_template in points_template:
            try:
                new_ids.append(point_template['id'])
            except KeyError:
                continue
        print("old_ids = ")
        print(old_ids)

        old_ids = set(old_ids)

        print("new_ids = ")
        print(new_ids)

        new_ids = set(new_ids)

        old_ids = old_ids.difference(new_ids)

        print(old_ids)

        for old_id in old_ids:
            PointTemplate.objects.get(id=old_id).delete()

    def add_points(self, bypass_sheet, student, point_template):

        point_data = dict()

        print('add_points')
        print(point_template.department.institute)

        if ((student.user.gender == point_template.gender or point_template.gender == 'None') and (
                point_template.department.institute is None or student.group.institute == point_template.department.institute)):

            point_data['title'] = point_template.title
            point_data['description'] = point_template.description
            point_data['gender'] = point_template.gender
            point_data['department'] = point_template.department
            point_data['bypass_sheet'] = bypass_sheet
            point_data['point_template'] = point_template

            self.create_required_documents(Point.objects.create(**point_data), point_template)

    def update_points_template(self, bypass_sheet_template, validated_data):
        points_template = validated_data.pop('points')

        old_ids = []

        old_points_template = PointTemplate.objects.filter(bypass_sheet_template=bypass_sheet_template)

        for old_point_template in old_points_template:
            old_ids.append(old_point_template.id)

        print('old_points_template')
        print(old_points_template)

        for point_data in points_template:
            try:
                print(point_data['title'])

                PointTemplate.objects.update_or_create(id=point_data['id'],
                                                               defaults={
                                                                   'title':point_data['title'],
                                                                   'description':point_data['description'],
                                                                   'gender':point_data['gender'],
                                                                   'bypass_sheet_template':bypass_sheet_template,
                                                                   'department':Department.objects.get(title=point_data['title'])
                                                               })
            except KeyError:

                 point_template_data = {
                    'title': point_data['title'],
                    'description': point_data['description'],
                    'gender': point_data['gender'],
                    'bypass_sheet_template': bypass_sheet_template,
                    'department': Department.objects.get(title=point_data['title'])
                 }

                 point_template = PointTemplate.objects.create(**point_template_data)

                 print(point_template)

                # obj, statement = PointTemplate.objects.update_or_create(id=None,
                #                                             defaults={
                #                                                 'title': point_data['title'],
                #                                                 'description': point_data['description'],
                #                                                 'gender': point_data['gender'],
                #                                                 'bypass_sheet_template': bypass_sheet_template,
                #                                                 'department': Department.objects.get(title=point_data['title'])
                #                                             })

                 bypass_sheets = BypassSheet.objects.filter(bypass_sheet_template=bypass_sheet_template)

                 for bypass_sheet in bypass_sheets:

                    self.add_points(bypass_sheet, bypass_sheet.student_id, point_template)

            point_template = PointTemplate.objects.get(title=point_data['title'], bypass_sheet_template=bypass_sheet_template)

            try:

                self.update_common_reasons(point_template, point_data.pop('commonReasons'))

            except KeyError:

                self.update_common_reasons(point_template, [])

            self.update_required_documents_template(point_template, point_data)

            self.update_upload_documents_format(point_template, point_data)

        self.delete_points_template(old_ids, bypass_sheet_template, points_template)

    def create_statement(self, bypass_sheet, bypass_sheet_template):

        statements_template_query = StatementsTemplate.objects.filter(bypass_sheet_template=bypass_sheet_template)

        statement_data = dict()

        for statement in statements_template_query:
            statement_data['file'] = statement.img
            statement_data['bypass_sheet'] = bypass_sheet

            Statement.objects.create(**statement_data)

            statement_data = dict()

    def create_required_documents(self, point, point_template):

        required_documents_templates = RequiredDocumentsTemplate.objects.filter(point_template=point_template)

        required_documents_data = dict()

        for required_documents_template in required_documents_templates:
            required_documents_data['img'] = required_documents_template.img
            required_documents_data['requiredDocumentsTemplate'] = required_documents_template
            required_documents_data['point'] = point

            RequiredDocuments.objects.create(**required_documents_data)

            required_documents_data = dict()

    def update_points(self, bypass_sheet, bypass_sheet_template):

        points_template_query = PointTemplate.objects.filter(bypass_sheet_template=bypass_sheet_template)

        print('update_points')

        for point_template in points_template_query:

            print(point_template.department.institute)

            if ((bypass_sheet.student_id.user.gender != point_template.gender and point_template.gender != 'None') or (point_template.department.institute is not None and bypass_sheet.student_id.group.institute != point_template.department.institute)):
                print('continue')
                continue

            Point.objects.update_or_create(title=point_template.title, bypass_sheet=bypass_sheet,
                                                   defaults={
                                                       'title':point_template.title,
                                                       'description': point_template.description,
                                                       'gender': point_template.gender,
                                                       'department':point_template.department,
                                                       'bypass_sheet': bypass_sheet,
                                                       'point_template': point_template
                                                   })

            point = Point.objects.get(title=point_template.title, bypass_sheet=bypass_sheet)

            self.create_required_documents(point, point_template)

    def create_points(self, bypass_sheet, bypass_sheet_template, student):
        points_template_query = PointTemplate.objects.filter(bypass_sheet_template=bypass_sheet_template)

        point_data = dict()

        print('create points')

        for point in points_template_query:

            print(point.department.institute)

            if ((student.user.gender != point.gender and point.gender != 'None') or (point.department.institute is not None and student.group.institute != point.department.institute)):
                print('continue')
                continue

            point_data['title'] = point.title
            point_data['description'] = point.description
            point_data['gender'] = point.gender
            point_data['department'] = point.department
            point_data['bypass_sheet'] = bypass_sheet
            point_data['point_template'] = point

            self.create_required_documents(Point.objects.create(**point_data), point)

            point_data = dict()

    def update_bypass_sheets(self, bypass_sheet_template, students, old_students_list):

        for old_student in old_students_list:

            if int(old_student.user.id) not in students:
                BypassSheet.objects.filter(bypass_sheet_template=bypass_sheet_template, student_id=old_student).delete()

        bypass_sheet_template.studentList.set(students)

        bypass_sheet_template.save()

        bypass_sheets = BypassSheet.objects.filter(bypass_sheet_template=bypass_sheet_template)

        for bypass_sheet in bypass_sheets:

            bypass_sheet.title = bypass_sheet_template.title
            bypass_sheet.educationForm = bypass_sheet_template.educationForm

            bypass_sheet.save()

            self.create_statement(bypass_sheet, bypass_sheet_template)
            self.update_points(bypass_sheet, bypass_sheet_template)

        bypass_sheet_data = dict()

        bypass_sheet_data['title'] = bypass_sheet_template.title
        bypass_sheet_data['educationForm'] = bypass_sheet_template.educationForm
        bypass_sheet_data['bypass_sheet_template'] = bypass_sheet_template

        for student_id in students:

            student = Student.objects.get(user=User.objects.get(id=student_id))

            bypass_sheet_data['student_id'] = student

            if ((BypassSheet.objects.filter(student_id = student, title=bypass_sheet_template.title)) or (student.educationForm != bypass_sheet_data['educationForm'])):
                continue

            bypass_sheet = BypassSheet.objects.create(**bypass_sheet_data)

            self.create_statement(bypass_sheet, bypass_sheet_template)

            self.create_points(bypass_sheet, bypass_sheet_template, student)

    def check_signing_points(self, bypass_sheet):

        points = Point.objects.filter(bypass_sheet=bypass_sheet)

        for point in points:
            if point.status != 'Подписано':
                return False
        return True

    def check_signing_bypass_sheets(self, bypass_sheet_template):

        bypass_sheets = BypassSheet.objects.filter(bypass_sheet_template=bypass_sheet_template)

        for bypass_sheet in bypass_sheets:

            student = bypass_sheet.student_id
            user = student.user

            if self.check_signing_points(bypass_sheet):
                bypass_sheet.status = 'Подписан'
                bypass_sheet.save()

                send_mail('MyDoc', 'Ваш обходной лист был успешно подписан', 'mydockemsu@gmail.com', [user.email])

            else:
                bypass_sheet.status = 'Не подписан'
                bypass_sheet.save()

    def create(self, validated_data):

        data = validated_data

        pk = self.context['id']

        bypass_sheet_validated_data = dict()

        bypass_sheet_validated_data.setdefault('title', data.pop('title'))
        bypass_sheet_validated_data.setdefault('educationForm', data.pop('educationForm'))

        bypass_sheet_template = BypassSheetTemplate.objects.get(id=pk)

        bypass_sheet_template.title = bypass_sheet_validated_data['title']

        bypass_sheet_template.educationForm = bypass_sheet_validated_data['educationForm']

        bypass_sheet_template.save()

        students = []

        old_students_list = bypass_sheet_template.studentList.all()

        try:
            for student in data.pop('studentList'):
                students.append(int(student))
        except KeyError:
            students = []

        self.update_statements_template(bypass_sheet_template, data)

        self.update_points_template(bypass_sheet_template, data)

        self.update_bypass_sheets(bypass_sheet_template, students, old_students_list)

        self.check_signing_bypass_sheets(bypass_sheet_template)

        return bypass_sheet_template

class UploadDocumentsSerializer(serializers.ModelSerializer):
    uploadedDocuments = serializers.ListField(write_only=True, allow_empty=True, required=False)

    class Meta:
        model = Point
        fields = ('title', 'uploadedDocuments')

    def __updateUploadedDocuments(self, point, files):
        send_mail_flag = False

        point.status = 'На подписании'
        point.save()

        department = point.department

        staffs = Staff.objects.filter(department=department)

        emails = []

        for staff in staffs:
            user = staff.user

            emails.append(user.email)

        #send_mail('MyDoc', 'Вам пришло заявление на подписание. Пожалуйста, проверьте ваш личный кабинет.', 'mydockemsu@gmail.com', emails)

        uploaded_document_data = dict()

        upload = UploadedDocuments.objects.filter(point=point).delete()

        for file in files:

            if isinstance(file, str):
                file_arr = file.split('/')

                file = file_arr[-2]+'/'+file_arr[-1]

            uploaded_document_data['img'] = file
            uploaded_document_data['point'] = point

            UploadedDocuments.objects.create(**uploaded_document_data)

            send_mail_flag = True

        if send_mail_flag:

            student = point.bypass_sheet.student_id

            mail_message = "Студент(-ка) " + student.user.fullname + " из группы " + student.group.name + " прислал(-а) документы на подписание. " \
                                                                                                                                     "Проверьте ваш личный кабинет."

            send_mail('MyDoc', mail_message,
                      'mydockemsu@gmail.com', emails)

    def create(self, validated_data):

        try:
            uploaded_documents_data = validated_data.pop('uploadedDocuments')
        except KeyError:
            uploaded_documents_data = []
        bypass_sheet = BypassSheet.objects.get(id=self.context['id'])

        point = Point.objects.get(title=validated_data['title'], bypass_sheet=bypass_sheet)

        self.__updateUploadedDocuments(point, uploaded_documents_data)

        return 1

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])

        data = dict()
        data['tokens'] = dict()

        data['tokens'].setdefault('access', str(refresh.access_token))

        if settings.SIMPLE_JWT['ROTATE_REFRESH_TOKENS']:
            if settings.SIMPLE_JWT['BLACKLIST_AFTER_ROTATION']:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data['tokens'].setdefault('refresh', str(refresh))
            data['tokens'].setdefault('expiresIn', int(round(time.time() * 1000)) + int(round(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].seconds * 1000)))

        return data

class StaffForDepartmentSerializer(serializers.ModelSerializer):

    fullname = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = ('fullname', 'email')

    def get_fullname(self, staff):
        user = staff.user

        return user.fullname

    def get_email(self, staff):
        return staff.user.email

class DepartmentsSerializer(serializers.ModelSerializer):

    staff = StaffForDepartmentSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ('title', 'address', 'institute', 'staff')

class UserBypassSheetSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    fullname = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    group = serializers.SlugRelatedField(slug_field='name', read_only=True)
    institute = serializers.SerializerMethodField()
    courseNumber = serializers.SerializerMethodField()
    bypassSheet = serializers.SerializerMethodField()
    isBaned = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ('id', 'fullname', 'email', 'recruitmentForm', 'status', 'group',
                  'institute', 'courseNumber', 'bypassSheet', 'isBaned')

    def get_isBaned(self, student):
        return student.user.is_baned

    def get_id(self, student):
        return student.user.id

    def get_fullname(self, student):
        return student.user.fullname

    def get_email(self, student):
        return student.user.email

    def get_institute(self, student):
        return student.group.institute.title

    def get_courseNumber(self, student):

        return student.group.course

    def get_bypassSheet(self, user):
        bypassSheetsName = self.context.get('bypassSheetsName')

        bypassSheets = BypassSheet.objects.filter(title=bypassSheetsName, student_id=user)

        sel_data = BypassSheetsSerializer().setup_eager_loading(bypassSheets)

        serializers = BypassSheetsSerializer(sel_data, context=self.context, many=True)

        return serializers.data

    @classmethod
    def setup_eager_loading(cls, queryset):
        queryset = queryset.select_related('user')

        queryset = queryset.prefetch_related('group')

        return queryset

class UserBypassSheetPointSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    fullname = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField(read_only=True)
    group = serializers.SlugRelatedField(slug_field='name', read_only=True)
    institute = serializers.SerializerMethodField(read_only=True)
    courseNumber = serializers.SerializerMethodField(read_only=True)
    point = serializers.SerializerMethodField(read_only=True)
    isBaned = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Student
        fields = ('id', 'fullname', 'email', 'recruitmentForm', 'status', 'group',
                  'institute', 'courseNumber', 'point', 'isBaned')

    def get_isBaned(self, student):
        return student.user.is_baned

    def get_id(self, student):
        return student.user.id

    def get_fullname(self, student):
        return student.user.fullname

    def get_email(self, student):
        return student.user.email

    def get_institute(self, student):
        return student.group.institute.title

    def get_courseNumber(self, student):

        return student.group.course

    def get_point(self, user):
        bypassSheetsName = self.context.get('bypassSheetsName')
        pointsName = self.context.get('pointName')

        bypassSheet = BypassSheet.objects.filter(title=bypassSheetsName, student_id=user).first()

        point = Point.objects.filter(title=pointsName, bypass_sheet=bypassSheet).first()

        serializers = PointSerializer(point, read_only=True)

        return serializers.data

    @classmethod
    def setup_eager_loading(cls, queryset):
        queryset = queryset.select_related('user')

        queryset = queryset.prefetch_related('group')

        return queryset

class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Statement
        fields = ("file",)

class StatementsTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = StatementsTemplate
        fields = ('img',)

class RequiredDocumentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequiredDocumentsTemplate
        fields = ('img',)

class PointTemplateSerializer(serializers.ModelSerializer):

    requiredDocuments = serializers.SerializerMethodField()
    uploadDocumentsFormat = serializers.SlugRelatedField(slug_field='title', many=True, read_only=True)
    commonReasons = serializers.SerializerMethodField()

    class Meta:
        model = PointTemplate
        fields = ('id', 'title', 'description', 'requiredDocuments', 'gender', 'uploadDocumentsFormat', 'commonReasons')

    def get_requiredDocuments(self, point_template):
        required_documents_template = RequiredDocumentsTemplate.objects.filter(point_template=point_template)

        files = []

        for required_document_template in required_documents_template:
            files.append(required_document_template.img.url)

        return files

    def get_commonReasons(self, point_template):
        common_reasons_in_string = point_template.commonReasons

        if common_reasons_in_string == "" or common_reasons_in_string == None:
            return []

        common_reasons_list = common_reasons_in_string.split('<separator>')

        common_reasons_list.pop()

        return common_reasons_list

class GetDeadlineSerializer(serializers.ModelSerializer):

    groupName = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Deadline
        fields = ('groupName', 'deadline')

class BypassSheetTemplateSerializer(serializers.ModelSerializer):

    statements = serializers.SerializerMethodField()
    points = PointTemplateSerializer(read_only=True, many=True)
    deadlines = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BypassSheetTemplate
        fields = ('id', 'title', 'educationForm', 'statements', 'points', 'studentList', 'deadlines')

    def get_statements(self, bypass_sheet_template):
        statements_template = StatementsTemplate.objects.filter(bypass_sheet_template=bypass_sheet_template)

        files = []

        for statement_template in statements_template:
            files.append(statement_template.img.url)

        return files

    def get_deadlines(self, bypass_sheet_template):

        deadlines = Deadline.objects.filter(bypass_sheets_template=bypass_sheet_template)

        serializer = GetDeadlineSerializer(deadlines, many=True, read_only=True)

        groups = Group.objects.all()

        data = serializer.data

        for group in groups:
            if len(Deadline.objects.filter(groupName=group, bypass_sheets_template=bypass_sheet_template)) == 0:
                data.append(OrderedDict({'groupName': group.name, 'deadline': ''}))

        return data

class PostStatementTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = StatementsTemplate
        fields = ('img',)

class PostRequiredDocumentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequiredDocumentsTemplate
        fields = ('img',)

class PostBypassSheetTemplateSerializer(serializers.ModelSerializer):

    statements = serializers.ListField(write_only=True, allow_empty=True, required=False)

    points = serializers.ListField(child=PostPointTemplateSerializer(write_only=True))

    studentList = serializers.ListField(write_only=True, allow_empty=True, allow_null=True, required=False)

    class Meta:
        model = BypassSheetTemplate
        fields = ('title', 'educationForm', 'statements', 'points', 'studentList')

    def create_statements_template(self, bypass_sheet_template, validated_data):

        try:
            statements_template = validated_data.pop('statements')
        except KeyError:
            statements_template = []

        statement_template_data = dict()

        for file in statements_template:
            statement_template_data['bypass_sheet_template'] = bypass_sheet_template
            statement_template_data['img'] = file
            StatementsTemplate.objects.create(**statement_template_data)

    def create_required_documents_template(self, point_template, point_data):

        try:
            required_documents = point_data.pop('requiredDocuments')
        except KeyError:
            required_documents = []

        required_documents_data = dict()

        for file in required_documents:
            required_documents_data['point_template'] = point_template
            required_documents_data['img'] = file

            RequiredDocumentsTemplate.objects.create(**required_documents_data)

            required_documents_data = dict()

    def create_upload_documents_format(self, point_template, point_data):

        try:
            upload_documents_format = point_data.pop('uploadDocumentsFormat')
        except KeyError:
            upload_documents_format = []

        upload_documents_format_data = dict()

        for upload_document_format in upload_documents_format:
            upload_documents_format_data['title'] = upload_document_format['title']
            upload_documents_format_data['point_template'] = point_template

            UploadDocumentsFormat.objects.create(**upload_documents_format_data)

            upload_documents_format_data = dict()

    def create_common_reasons(self, point_template, common_reasons):

        common_reasons_in_string = ""

        for common_reason in common_reasons:
            common_reasons_in_string += common_reason + "<separator>"

        point_template.commonReasons = common_reasons_in_string

        point_template.save()

    def create_points_template(self, bypass_sheet_template, validated_data):

        points_template = validated_data.pop('points')

        points_template_data = dict()

        for point in points_template:
            points_template_data['title'] = point['title']
            points_template_data['description'] = point['description']
            points_template_data['gender'] = point['gender']
            points_template_data['bypass_sheet_template'] = bypass_sheet_template
            points_template_data['department'] = Department.objects.get(title=point['title'])

            point_template = PointTemplate.objects.create(**points_template_data)

            try:
                self.create_common_reasons(point_template, point.pop('commonReasons'))
            except KeyError:

                point_template.commonReasons = ""

                point_template.save()

            self.create_required_documents_template(point_template, point)
            self.create_upload_documents_format(point_template, point)

    def create_required_documents(self, point, point_template):
        required_documents_templates = RequiredDocumentsTemplate.objects.filter(point_template=point_template)

        required_documents_data = dict()

        for required_documents_template in required_documents_templates:
            required_documents_data['img'] = required_documents_template.img.url
            required_documents_data['requiredDocumentsTemplate'] = required_documents_template
            required_documents_data['point'] = point

            RequiredDocuments.objects.create(**required_documents_data)

    def create_points(self, bypass_sheet, bypass_sheet_template, student):

        points_template_query = PointTemplate.objects.filter(bypass_sheet_template=bypass_sheet_template).prefetch_related('department__institute', 'department')

        point_data = dict()

        for point in points_template_query:
            gender = point.gender
            if ((student.user.gender != gender and gender != 'None') or (point.department.institute is not None and student.group.institute != point.department.institute)):
                continue

            point_data['title'] = point.title
            point_data['description'] = point.description
            point_data['gender'] = gender
            point_data['department'] = point.department
            point_data['bypass_sheet'] = bypass_sheet
            point_data['point_template'] = point

            self.create_required_documents(Point.objects.create(**point_data), point)

    # def create_statement(self, bypass_sheet, bypass_sheet_template):
    #     statements_template_query = StatementsTemplate.objects.filter(bypass_sheet_template=bypass_sheet_template)
    #
    #     statement_data = dict()
    #
    #     for statement in statements_template_query:
    #         statement_data['bypass_sheet'] = bypass_sheet
    #         # statement_data['statement_template'] = statement
    #
    #         Statement.objects.create(**statement_data)

    def create_bypass_sheets(self, bypass_sheet_template):
        studentQuery = bypass_sheet_template.studentList.all().select_related('')

        bypass_sheet_data = dict()

        bypass_sheet_data['title'] = bypass_sheet_template.title
        bypass_sheet_data['educationForm'] = bypass_sheet_template.educationForm
        bypass_sheet_data['bypass_sheet_template'] = bypass_sheet_template

        for student in studentQuery:
            if student.educationForm != bypass_sheet_data['educationForm']:
                continue
            bypass_sheet_data['student_id'] = student

            bypass_sheet = BypassSheet.objects.create(**bypass_sheet_data)

            # self.create_statement(bypass_sheet, bypass_sheet_template)

            self.create_points(bypass_sheet, bypass_sheet_template, student)

    def create(self, validated_data):
        bypass_sheet_validated_data = dict()

        bypass_sheet_validated_data.setdefault('title', validated_data.pop('title'))
        bypass_sheet_validated_data.setdefault('educationForm', validated_data.pop('educationForm'))

        if BypassSheetTemplate.objects.filter(title=bypass_sheet_validated_data['title'], educationForm=bypass_sheet_validated_data['educationForm']).first():
            raise BypassSheetTemplateExistException

        bypass_sheet_template = BypassSheetTemplate.objects.create(**bypass_sheet_validated_data)

        try:
            # students = map(int, validated_data.pop('studentList'))
            students = validated_data.pop('studentList')
        except KeyError:
            students = []

        # try:
        #     for student in validated_data.pop('studentList'):
        #         students.append(int(student))
        # except KeyError:
        #     students = []

        bypass_sheet_template.studentList.set(students)

        self.create_statements_template(bypass_sheet_template, validated_data)

        self.create_points_template(bypass_sheet_template, validated_data)

        self.create_bypass_sheets(bypass_sheet_template)

        return bypass_sheet_template

class UnregisteredStudentSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField(read_only=True, required=False)
    institute = serializers.SerializerMethodField(read_only=True, required=False)

    class Meta:
        model = User
        fields = ('fullname', 'group', 'institute')

    def get_group(self, user):
        student = Student.objects.get(user=user)

        group = Group.objects.get(id=student.group.id)

        return group.name

    def get_institute(self, user):
        student = Student.objects.get(user=user)

        group = Group.objects.get(id=student.group.id)

        institute = Institute.objects.get(id=group.institute.id)

        return institute.title

class CheckAccessSerializer(serializers.Serializer):

    accessToken = serializers.CharField(write_only=True)
    role = serializers.ListField(write_only=True)

    def validate(self, attrs):

        data = dict()

        data['hasAccess'] = False

        accessToken = attrs['accessToken']

        user_id = jwt.decode(accessToken, settings.SECRET_KEY, algorithms="HS256")['user_id']

        user_role = User.objects.get(id=user_id).status

        roles = attrs['role']

        for role in roles:
            if user_role == role:
                data['hasAccess'] = True
                break

        return data

    def save(self, **kwargs):
        pass

class GetBypassSheetsSchemaDeadlinesSerializer(serializers.ModelSerializer):

    deadlines = serializers.SerializerMethodField()

    class Meta:
        model = BypassSheetTemplate
        fields = ('id', 'title', 'deadlines')

    def get_deadlines(self, bypass_sheet_template):

        user = self.context.get('user')

        staff = Staff.objects.get(user=user)

        institute = staff.department.institute

        if institute is not None:
            groups = Group.objects.filter(institute=institute)
            deadlines = Deadline.objects.filter(bypass_sheets_template=bypass_sheet_template,
                                                groupName__institute=institute)
        else:
            groups = Group.objects.all()
            deadlines = Deadline.objects.filter(bypass_sheets_template=bypass_sheet_template)

        serializer = GetDeadlineSerializer(deadlines, many=True, read_only=True)

        data = serializer.data

        for group in groups:
            if len(Deadline.objects.filter(groupName=group, bypass_sheets_template=bypass_sheet_template))==0:
                data.append(OrderedDict({'groupName':group.name, 'deadline':''}))

        return data

class PatchBypassSheetsSchemaDeadlinesSerializer(serializers.Serializer):

    data = serializers.ListField(write_only=True)

    def validate(self, attrs):

        print('create here')

        print(attrs)

        id = self.context.get('id')

        bypass_sheet_schema = BypassSheetTemplate.objects.get(id=id)

        for deadline in attrs['data']:

            group = Group.objects.get(name=deadline['groupName'])

            Deadline.objects.update_or_create(groupName=group, bypass_sheets_template=bypass_sheet_schema,
                                              defaults = {
                                                  'groupName' : group,
                                                  'deadline' : deadline['deadline'],
                                                  'bypass_sheets_template' : bypass_sheet_schema
                                              })
        return attrs

    def save(self, **kwargs):
        pass