from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import (
    User, Department, Group, Institute,
    Module, Point, Staff, Student,
)

class RegistrationStudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

    #token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

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
        fields = ('username', 'email', 'password', 'staff_id')

    def create(self, validated_data):
        return User.objects.create_staff(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    username = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'token': user.token,
        }

class RecursiveSerializer(serializers.Serializer):

    def to_representation(self, value):
        serializer = self.parent.__class__(value, context=self.context)
        return serializer.data

class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = "__all__"

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

class PointSerializer(serializers.ModelSerializer):

    class Meta:
        model = Point
        fields = "__all__"

class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        fields = "__all__"

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "email")

class GetBypassSheetsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Module
        exclude = ("student_id",)

class PostByPassSheetsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Module
        fields = "__all__"

class GetByPassSheetsDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Point
        exclude = ("module_id",)
