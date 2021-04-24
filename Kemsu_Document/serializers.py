from django.contrib.auth import authenticate
from psycopg2.compat import text_type
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from djangoProject import settings
from django.utils.text import gettext_lazy as _

from rest_framework.serializers import Serializer, FileField
from .exceptions import GroupNotFoundError, ThisUserIsAlreadyExistException, ThisEmailIsAlreadyExistError
from .models import (
    User, Department, Group, Institute,
    Module, Point, Statement, UploadedDocuments, RequiredDocuments, Staff, Student,
)

# class RegistrationStudentSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(
#         max_length=128,
#         min_length=8,
#         write_only=True,
#     )
#
#     class Meta:
#         model = User
#         fields = ('fullname', 'email', 'password', 'group', 'status')
#
#     def create(self, validated_data):
#          return User.objects.create_student(**validated_data)

class RegistrationUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

    class Meta:
        model = User
        fields = ('fullname', 'email', 'password')

class RegistrationStaffSerializer(serializers.ModelSerializer):

    user = RegistrationUserSerializer(required=True, read_only=False)

    class Meta:
        model = Staff
        fields = ('user', 'department')

    def create(self, validated_data):
        user_data = validated_data['user']
        if user_data:
            staff = User.objects.create_staff(**user_data)
            validated_data['user'] = staff
        return Staff.objects.create(**validated_data)

class RegistrationStudentSerializer(serializers.ModelSerializer):

    #user = RegistrationUserSerializer(required=True, read_only=False)
    group = serializers.CharField(max_length=50)
    fullname = serializers.CharField(max_length=50)
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )
    email = serializers.EmailField(max_length=50)

    class Meta:
        model = Student
        #fields = ('user', 'group', 'recordBookNumber')
        fields = ('fullname', 'password', 'email', 'group', 'recordBookNumber')

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
            student = User.objects.create_student(**user_data)
        except Exception:
            raise ThisEmailIsAlreadyExistError

        validated_data['user'] = student

        validated_data['group'] = group

        return Student.objects.create(**validated_data)

class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        exclude = ('id',)

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

class PointSerializer(serializers.ModelSerializer):

    uploadedDocuments = UploadedDocumentSerializer(many=True, read_only=True)
    requiredDocuments = RequiredDocumentsSerializer(many=True, read_only=True)

    class Meta:
        model = Point
        fields = ("title", "status", "uploadedDocuments", "requiredDocuments", "staff")

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'fullname', 'email')

class StudentSerializer(serializers.ModelSerializer):

    # departments = DepartmentSerializer(many=True, read_only=True)
    # institute = serializers.SlugRelatedField(slug_field='name', read_only=True)
    # group = serializers.SlugRelatedField(slug_field='name', read_only=True)
    # group = serializers.SlugRelatedField(slug_field='name', read_only=True)
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




class PostByPassSheetsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Module
        fields = "__all__"

class GetByPassSheetsDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Point
        exclude = ("module_id",)

class TokenEmailSerializer(Serializer):
    username_field = User.EMAIL_FIELD

    def __init__(self, *args, **kwargs):
        super(TokenEmailSerializer, self).__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        # self.user = authenticate(**{
        #     self.username_field: attrs[self.username_field],
        #     'password': attrs['password'],
        # })
        self.user = User.objects.filter(email=attrs[self.username_field]).first()
        print(self.user)

        if not self.user:
            raise ValidationError('The user is not valid.')

        if self.user:
            if not self.user.check_password(attrs['password']):
                raise ValidationError('Incorrect credentials.')
        print(self.user)
        # Prior to Django 1.10, inactive users could be authenticated with the
        # default `ModelBackend`.  As of Django 1.10, the `ModelBackend`
        # prevents inactive users from authenticating.  App designers can still
        # allow inactive users to authenticate by opting for the new
        # `AllowAllUsersModelBackend`.  However, we explicitly prevent inactive
        # users from authenticating to enforce a reasonable policy and provide
        # sensible backwards compatibility with older Django versions.
        if self.user is None or not self.user.is_active:
            raise ValidationError('No active account found with the given credentials')

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

#-----Авторизация по username

class TokenUsernameSerializer(Serializer):
    username_field = User.USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super(TokenUsernameSerializer, self).__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        # self.user = authenticate(**{
        #     self.username_field: attrs[self.username_field],
        #     'password': attrs['password'],
        # })
        self.user = User.objects.filter(username=attrs[self.username_field]).first()
        print(self.user)

        if not self.user:
            raise ValidationError('The user is not valid.')

        if self.user:
            if not self.user.check_password(attrs['password']):
                raise ValidationError('Incorrect credentials.')
        print(self.user)
        # Prior to Django 1.10, inactive users could be authenticated with the
        # default `ModelBackend`.  As of Django 1.10, the `ModelBackend`
        # prevents inactive users from authenticating.  App designers can still
        # allow inactive users to authenticate by opting for the new
        # `AllowAllUsersModelBackend`.  However, we explicitly prevent inactive
        # users from authenticating to enforce a reasonable policy and provide
        # sensible backwards compatibility with older Django versions.
        if self.user is None or not self.user.is_active:
            raise ValidationError('No active account found with the given credentials')

        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplemented(
            'Must implement `get_token` method for `MyTokenObtainSerializer` subclasses')


class TokenUsernamePairSerializer(TokenUsernameSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super(TokenUsernamePairSerializer, self).validate(attrs)
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

class RefreshTokenSerializer(serializers.Serializer):
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

class DepartmentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ('title','address','institute')

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fields = ("file", "title",)