from datetime import time

from psycopg2.compat import text_type
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
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
    Module, Point, Statement, UploadedDocuments, RequiredDocuments, Staff, Student,
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
        user_data.setdefault('fullname', validated_data.pop('fullname'))
        user_data.setdefault('email', validated_data.pop('email'))
        user_data.setdefault('password', validated_data.pop('password'))

        fullnameIsExist = User.objects.filter(fullname=user_data['fullname'])

        if len(fullnameIsExist) != 0:
            raise ThisUserIsAlreadyExistException
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

    recordBookNumber = serializers.CharField(max_length=50, write_only=True, allow_blank=True)

    class Meta:
        model = Student
        fields = ('fullname', 'password', 'email', 'group', 'recordBookNumber', 'tokens')

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

    def create(self, validated_data):
        user_data = dict()
        user_data.setdefault('fullname', validated_data.pop('fullname'))
        user_data.setdefault('email', validated_data.pop('email'))
        user_data.setdefault('password', validated_data.pop('password'))

        fullnameIsExist = User.objects.filter(fullname=user_data['fullname'])

        recordBookNumber = validated_data['recordBookNumber']

        if len(fullnameIsExist) != 0 and recordBookNumber == "":
            raise ThisUserIsAlreadyExistException

        try:
            group = Group.objects.get(title=validated_data['group'])
        except Exception:
            raise GroupNotFoundError
        try:
            user = User.objects.create_student(**user_data)
        except Exception:
            raise ThisEmailIsAlreadyExistError

        validated_data['user'] = user

        validated_data['group'] = group

        Student.objects.create(**validated_data)

        return user

class GroupSerializer(serializers.ModelSerializer):

    institute = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = Group
        fields = ('title', 'institute')

class InstituteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Institute
        fields = "__all__"

class ModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Module
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
    requiredDocuments = RequiredDocumentsSerializer(many=True, read_only=True)
    staff = StaffSerializer(read_only=True)

    class Meta:
        model = Point
        fields = ("title", "status", "uploadedDocuments", "requiredDocuments", "staff")

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'fullname', 'email')

class StudentSerializer(serializers.ModelSerializer):

    user = UserSerializer(required=False, read_only=True)
    group = GroupSerializer(required=False, read_only=True)

    class Meta:
        model = Student
        fields = ('user', 'group')

class StatementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Statement
        fields = ("title", "img")

class BypassSheetsSerializer(serializers.ModelSerializer):

    statements = StatementSerializer(many=True, read_only=True)
    points = PointSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ("title", "statements", "points", )

class PostStatementsSerializer(serializers.ModelSerializer):

    title = serializers.CharField(max_length=50, write_only=True)
    img = serializers.ImageField(use_url=True, allow_empty_file=True, allow_null=True)

    class Meta:
        model = Statement
        fields = ('title', 'img')

class PostByPassSheetsSerializer(serializers.ModelSerializer):

    statements = PostStatementsSerializer(many=True, write_only=True)

    title = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        model = Module
        fields = ('title', 'statements')

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

        module = Module.objects.create(**validated_data)

        self.statementsCreate(statements_data, module)

        return module

class TokenEmailSerializer(Serializer):
    #username_field = User.EMAIL_FIELD

    def __init__(self, *args, **kwargs):
        super(TokenEmailSerializer, self).__init__(*args, **kwargs)

        self.fields['username_field'] = serializers.CharField()
        self.fields['password'] = serializers.CharField(max_length=128, write_only=True)
        self.fields['recordBookNumber'] = serializers.CharField(max_length=128, write_only=True, allow_blank=True, allow_null=True)

    def getUser(self, attrs):
        email_or_fullname = attrs['username_field']
        if email_or_fullname.find('@') != -1:
             return User.objects.filter(email=attrs['username_field']).first()
        else:
            users = User.objects.filter(fullname=email_or_fullname)
            if len(users) > 1:
                recordBookNumber = attrs['recordBookNumber']

                if recordBookNumber == '':
                    raise ValidationError('More than 1 user with this name is registered in this system. If you are student - please enter the correct recordbook number, or log in using your email')

                user = None

                for not_confirmed_student in users:
                    user = Student.objects.filter(user=not_confirmed_student, recordBookNumber=recordBookNumber).first()
                    if user:
                        break

                if not user:
                    raise ValidationError('More than 1 user with this name is registered in this system. If you are student - please enter the correct recordbook number, or log in using your email')

                return User.objects.get(id=user.user.id)
            else:
                return users.first()

    def validate(self, attrs):
        # self.user = authenticate(**{
        #     self.username_field: attrs[self.username_field],
        #     'password': attrs['password'],
        # })

        #self.user = User.objects.filter(email=attrs[self.username_field]).first()

        self.user = self.getUser(attrs)

        if not self.user:
            raise ValidationError('The user is not valid.')

        if self.user:
            if not self.user.check_password(attrs['password']):
                raise ValidationError('Incorrect credentials.')
        # Prior to Django 1.10, inactive users could be authenticated with the
        # default `ModelBackend`.  As of Django 1.10, the `ModelBackend`
        # prevents inactive users from authenticating.  App designers can still
        # allow inactive users to authenticate by opting for the new
        # `AllowAllUsersModelBackend`.  However, we explicitly prevent inactive
        # users from authenticating to enforce a reasonable policy and provide
        # sensible backwards compatibility with older Django versions.
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
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super(TokenEmailPairSerializer, self).validate(attrs)
        refresh = self.get_token(self.user)

        data['refresh'] = text_type(refresh)
        data['access'] = text_type(refresh.access_token)
        data['expiresIn'] = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].seconds
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

        data = {'access': str(refresh.access_token)}

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

            data['refresh'] = str(refresh)
            data['expiresIn'] = int(round(time.time() * 1000)) + int(round(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].seconds * 1000))

        return data

class LoginSerializer(serializers.Serializer):
    email_or_fullname = serializers.CharField(write_only=True)

    password = password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

    recordBookNumber = serializers.CharField(allow_blank=True, write_only=True)

    def get_tokens(self, user):
        return RefreshToken.for_user(user)

    def emailLogin(self, attrs):
        try:
            user = User.objects.get(email=attrs['email_or_fullname'])
        except Exception:
            raise UserWithThisEmailDoesNotExistException
        if not user.check_password(attrs['password']):
            raise ValidationError('Incorrect credentials.')
        return self.get_tokens(user)

    def fullnameLogin(self, attrs):
        pass

    def validate(self, attrs):
        email_or_fullname = attrs['email_or_fullname']
        # if email_or_fullname.find('@') == -1:
        #     tokens = self.fullnameLogin(attrs)
        # else:
        #     tokens = self.emailLogin(attrs)
        tokens = self.emailLogin(attrs)
        data = {'access': str(tokens.access_token)}
        return data