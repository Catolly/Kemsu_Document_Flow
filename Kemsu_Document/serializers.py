from django.contrib.auth import authenticate
from psycopg2.compat import text_type
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from djangoProject import settings

from .models import (
    User, Department, Group, Institute,
    Module, Point, Statement, UploadedDocuments, RequiredDocuments,
)

class RegistrationStudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

    class Meta:
        model = User
        fields = ('fullname', 'email', 'password', 'group', 'status')

    # def get_tokens(self, user):
    #     tokens = RefreshToken.for_user(user)
    #     refresh = text_type(tokens)
    #     access = text_type(tokens.access_token)
    #     data = {
    #         "refresh": refresh,
    #         "access": access
    #     }
    #     return data

    def create(self, validated_data):
         return User.objects.create_student(**validated_data)

class RegistrationStaffSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

    #token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('fullname', 'email', 'password', 'department_id', 'status')

    def create(self, validated_data):
        return User.objects.create_staff(**validated_data)

class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        exclude = ('id',)

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = "__all__"

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
        fields = ("title", "status", "uploadedDocuments", "requiredDocuments")

class UserSerializer(serializers.ModelSerializer):

    departments = DepartmentSerializer(many=True, read_only=True)
    institute = serializers.SlugRelatedField(slug_field='name', read_only=True)
    group = serializers.SlugRelatedField(slug_field='name', read_only=True)
    ol = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "fullname", "email", 'departments', 'group', 'institute', 'ol')

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

