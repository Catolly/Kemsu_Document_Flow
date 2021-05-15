from datetime import time, datetime
import json

import jwt
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
    DepartmentNotFoundException, UserWithThisFullNameDoesNotExistException, UserWithThisEmailDoesNotExistException
from .models import (
    User, Department, Group, Institute,
    BypassSheet, Point, Statement, UploadedDocuments, RequiredDocuments, Staff, Student, BypassSheetTemplate,
    StatementsTemplate, PointTemplate, UploadDocumentsFormat,
)

class RegistrationStaffSerializer(serializers.ModelSerializer):

    department = serializers.CharField(max_length=50, write_only=True)
    fullname = serializers.CharField(max_length=50, write_only=True)
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )
    email = serializers.EmailField(max_length=50, write_only=True)

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

    group = serializers.CharField(max_length=50, write_only=True)
    fullname = serializers.CharField(max_length=50, write_only=True)
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )
    email = serializers.EmailField(max_length=50, write_only=True)

    tokens = serializers.SerializerMethodField()

    id = serializers.SerializerMethodField()

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
        group = Group.objects.filter(name=validated_data['group']).first()

        student_data = Student.objects.filter(group=group)

        for student in student_data:
            user = User.objects.filter(fullname=validated_data['fullname'], id=student.user.id).first()
            if user:
                break

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
    courseNumber = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ('name', 'institute', 'courseNumber')

    def get_courseNumber(self, group):
        recruitment_data = group.recruitment_date

        return int(((datetime.now().date() - recruitment_data).days) // 365.2425) + 1

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
        fields = ("title", "img")

class RequiredDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequiredDocuments
        fields = ("title", "img")

class StaffSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField('fullname', read_only=True)

    class Meta:
        model = Staff
        fields = ('user', )

class PointSerializer(serializers.ModelSerializer):

    uploadedDocuments = UploadedDocumentSerializer(many=True, read_only=True)
    staff = StaffSerializer(read_only=True)
    requiredDocuments = RequiredDocumentsSerializer(many=True, read_only=True)

    class Meta:
        model = Point
        fields = ("title", "status", "uploadedDocuments", "staff", "rejectReason", 'requiredDocuments')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'fullname', 'email')

class StatementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Statement
        fields = ("title", "img")

class BypassSheetsSerializer(serializers.ModelSerializer):

    statements = StatementSerializer(many=True, read_only=True)
    points = PointSerializer(many=True, read_only=True)

    class Meta:
        model = BypassSheet
        fields = ("name", "statements", "points", "status")

    # def get_points(self, BypassSheet):
    #     # bypassSheetsName = self.context.get('bypassSheetsName')
    #     #
    #     # bypassSheets = BypassSheet.objects.filter(name=bypassSheetsName, student_id=user)
    #     #
    #     # serializers = BypassSheetsSerializer(bypassSheets, context=self.context, many=True)
    #     #
    #     # return serializers.data
    #     pointsName = self.context.get('pointName')
    #     print(pointsName)
    #     if pointsName != "":
    #         points = Point.objects.filter(title=pointsName, bypass_sheet=BypassSheet)
    #     else:
    #         points = Point.objects.filter(bypass_sheet=BypassSheet)
    #
    #     serializers = PointSerializer(points, many=True, read_only=True)

        # return serializers.data

class StudentSerializer(serializers.ModelSerializer):

    # user = UserSerializer(required=False, read_only=True)
    # group = GroupSerializer(required=False, read_only=True)
    # bypassSheet = BypassSheetsSerializer(required=False, read_only=True, many=True)
    #
    # class Meta:
    #     model = Student
    #     fields = ('user', 'group', 'educationForm', 'status', 'bypassSheet')

    id = serializers.SerializerMethodField()
    fullname = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    group = serializers.SlugRelatedField(slug_field='name', read_only=True)
    institute = serializers.SerializerMethodField()
    courseNumber = serializers.SerializerMethodField()
    bypassSheet = BypassSheetsSerializer(required=False, read_only=True, many=True)

    class Meta:
        model = Student
        fields = ('id', 'fullname', 'email', 'recruitmentForm', 'status', 'group',
                  'institute', 'courseNumber', 'bypassSheet')

    def get_id(self, student):
        return student.user.id

    def get_fullname(self, student):
        return student.user.fullname

    def get_email(self, student):
        return student.user.email

    def get_institute(self, student):
        return student.group.institute.title

    def get_courseNumber(self, student):
        recruitment_data = student.group.recruitment_date

        return int(((datetime.now().date() - recruitment_data).days)//365.2425)+1

class PostStatementsSerializer(serializers.ModelSerializer):

    title = serializers.CharField(max_length=50, write_only=True)
    img = serializers.ImageField(use_url=True, allow_empty_file=True, allow_null=True)

    class Meta:
        model = Statement
        fields = ('title', 'img')

class PostByPassSheetsSerializer(serializers.ModelSerializer):

    statements = PostStatementsSerializer(many=True, write_only=True)

    name = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        model = BypassSheet
        fields = ('name', 'statements')

    def statementsCreate(self, statements_data, module):

        for statement_data in statements_data:
            statement_data['module'] = module
            Statement.objects.create(**statement_data)

    def create(self, validated_data):
        user = None
        request = self.context.get("request")

        if request and hasattr(request, "user"):
            user = request.user

        statements_data_ordered_dict = validated_data.pop('statements')

        statements_data = []

        for statement_data in statements_data_ordered_dict:
            statements_data.append(dict(statement_data))

        student = Student.objects.get(user=user.id)

        validated_data['student_id'] = student

        module = BypassSheet.objects.create(**validated_data)

        self.statementsCreate(statements_data, module)

        self.__createPoints(module)

        return module

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
            raise ValidationError('The user is not valid.')

        if self.user:
            if not self.user.check_password(attrs['password']):
                raise ValidationError('Incorrect credentials.')

        if self.user is None:
            raise ValidationError('No active account found with the given credentials')
        if not self.user.is_active:
            raise ValidationError('Your account has not been verified by the administrator')

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

class DepartmentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ('title', 'address', 'institute')

class UserBypassSheetSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    fullname = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    group = serializers.SlugRelatedField(slug_field='name', read_only=True)
    institute = serializers.SerializerMethodField()
    courseNumber = serializers.SerializerMethodField()
    bypassSheet = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ('id', 'fullname', 'email', 'recruitmentForm', 'status', 'group',
                  'institute', 'courseNumber', 'bypassSheet')

    def get_id(self, student):
        return student.user.id

    def get_fullname(self, student):
        return student.user.fullname

    def get_email(self, student):
        return student.user.email

    def get_institute(self, student):
        return student.group.institute.title

    def get_courseNumber(self, student):
        recruitment_data = student.group.recruitment_date

        return int(((datetime.now().date() - recruitment_data).days) // 365.2425) + 1

    def get_bypassSheet(self, user):
        bypassSheetsName = self.context.get('bypassSheetsName')

        bypassSheets = BypassSheet.objects.filter(name=bypassSheetsName, student_id=user)

        serializers = BypassSheetsSerializer(bypassSheets, context=self.context, many=True)

        return serializers.data

class UserBypassSheetPointSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    fullname = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    group = serializers.SlugRelatedField(slug_field='name', read_only=True)
    institute = serializers.SerializerMethodField()
    courseNumber = serializers.SerializerMethodField()
    point = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ('id', 'fullname', 'email', 'recruitmentForm', 'status', 'group',
                  'institute', 'courseNumber', 'point')

    def get_id(self, student):
        return student.user.id

    def get_fullname(self, student):
        return student.user.fullname

    def get_email(self, student):
        return student.user.email

    def get_institute(self, student):
        return student.group.institute.title

    def get_courseNumber(self, student):
        recruitment_data = student.group.recruitment_date

        return int(((datetime.now().date() - recruitment_data).days) // 365.2425) + 1

    def get_point(self, user):
        bypassSheetsName = self.context.get('bypassSheetsName')
        pointsName = self.context.get('pointName')

        bypassSheets = BypassSheet.objects.filter(name=bypassSheetsName, student_id=user)

        points = Point.objects.filter(title=None)
        for bypassSheet in bypassSheets:
            points |= Point.objects.filter(title=pointsName, bypass_sheet=bypassSheet)

        serializers = PointSerializer(points, many=True, read_only=True)

        return serializers.data
class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Statement
        fields = ("file", "title")

class StatementsTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = StatementsTemplate
        fields = ('title', 'img')

class RequiredDocumentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequiredDocuments
        fields = ('title', 'img')

class PointTemplateSerializer(serializers.ModelSerializer):

    requiredDocuments = RequiredDocumentsSerializer(many=True, read_only=True)

    class Meta:
        model = PointTemplate
        fields = ('title', 'description', 'requiredDocuments')

class BypassSheetTemplateSerializer(serializers.ModelSerializer):

    statements = StatementsTemplateSerializer(required=False, read_only=True, many=True)
    points = PointTemplateSerializer(required=False, read_only=True, many=True)

    class Meta:
        model = BypassSheetTemplate
        fields = ('name', 'educationForm', 'statements', 'points')

class PostStatementTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = StatementsTemplate
        fields = ('title', 'img')

class PostRequiredDocumentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequiredDocuments
        fields = ('title', 'img')

class PostUploadDocumentsFormatSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadDocumentsFormat
        fields = ('title', 'format')

class PostPointTemplateSerializer(serializers.ModelSerializer):

    requiredDocuments = PostRequiredDocumentsSerializer(many=True, write_only=True)
    uploadDocumentsFormat = PostUploadDocumentsFormatSerializer(many=True, write_only=True)

    class Meta:
        model = PointTemplate
        fields = ('title', 'description', 'requiredDocuments', 'gender', 'uploadDocumentsFormat')

class PostBypassSheetTemplateSerializer(serializers.ModelSerializer):

    statements = PostStatementTemplateSerializer(many=True, write_only=True)
    points = PostPointTemplateSerializer(many=True, write_only=True)
    studentList = serializers.ListField(write_only=True, allow_empty=True)

    class Meta:
        model = BypassSheetTemplate
        fields = ('name', 'educationForm', 'statements', 'points', 'studentList')

    def create_statements_template(self, bypass_sheet_template, validated_data):
        statements_template = validated_data.pop('statements')

        statement_template_data = dict()

        for statement in statements_template:
            statement_template_data['title'] = statement['title']
            statement_template_data['bypass_sheet_template'] = bypass_sheet_template
            StatementsTemplate.objects.create(**statement_template_data)
            statement_template_data = dict()

    def create_required_documents(self, point_template, point_data):
        required_documents = point_data.pop('requiredDocuments')

        required_documents_data = dict()

        for required_document in required_documents:
            required_documents_data['title'] = required_document['title']
            required_documents_data['point_template'] = point_template

            RequiredDocuments.objects.create(**required_documents_data)

            required_documents_data = dict()

    def create_upload_documents_format(self, point_template, point_data):
        upload_documents_format = point_data.pop('uploadDocumentsFormat')

        upload_documents_format_data = dict()

        for upload_document_format in upload_documents_format:
            upload_documents_format_data['title'] = upload_document_format['title']
            upload_documents_format_data['format'] = upload_document_format['format']
            upload_documents_format_data['point_template'] = point_template

            UploadDocumentsFormat.objects.create(**upload_documents_format_data)

            upload_documents_format_data = dict()

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

            self.create_required_documents(point_template, point)
            self.create_upload_documents_format(point_template, point)

            points_template_data = dict()

    def create_points(self, bypass_sheet, bypass_sheet_template):
        points_template_query = PointTemplate.objects.filter(bypass_sheet_template=bypass_sheet_template)

        point_data = dict()

        for point in points_template_query:
            point_data['title'] = point.title
            point_data['description'] = point.description
            point_data['gender'] = point.gender
            point_data['department'] = point.department
            point_data['bypass_sheet'] = bypass_sheet

            Point.objects.create(**point_data)

            point_data = dict()

    def create_statement(self, bypass_sheet, bypass_sheet_template):
        statements_template_query = StatementsTemplate.objects.filter(bypass_sheet_template=bypass_sheet_template)

        statement_data = dict()

        for statement in statements_template_query:
            statement_data['title'] = statement.title
            statement_data['img'] = statement.img
            statement_data['bypass_sheet'] = bypass_sheet

            Statement.objects.create(**statement_data)

            statement_data = dict()

    def create_bypass_sheets(self, bypass_sheet_template):
        studentQuery = bypass_sheet_template.studentList.all()

        bypass_sheet_data = dict()

        bypass_sheet_data['name'] = bypass_sheet_template.name
        bypass_sheet_data['educationForm'] = bypass_sheet_template.educationForm

        for student in studentQuery:
            bypass_sheet_data['student_id'] = student

            bypass_sheet = BypassSheet.objects.create(**bypass_sheet_data)

            self.create_statement(bypass_sheet, bypass_sheet_template)

            self.create_points(bypass_sheet, bypass_sheet_template)

    def create(self, validated_data):
        bypass_sheet_validated_data = dict()

        bypass_sheet_validated_data.setdefault('name', validated_data.pop('name'))
        bypass_sheet_validated_data.setdefault('educationForm', validated_data.pop('educationForm'))
        bypass_sheet_template = BypassSheetTemplate.objects.create(**bypass_sheet_validated_data)
        bypass_sheet_template.studentList.set(validated_data.pop('studentList'))

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
        student = Student.objects.filter(user=user).first()

        group = Group.objects.filter(id=student.group.id).first()

        return group.name

    def get_institute(self, user):
        student = Student.objects.filter(user=user).first()

        group = Group.objects.filter(id=student.group.id).first()

        institute = Institute.objects.filter(id=group.institute.id).first()

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