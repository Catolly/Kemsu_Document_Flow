from django.shortcuts import redirect, render
from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from Kemsu_Document.exceptions import GroupNotFoundError, ThisUserIsAlreadyExistException, ThisEmailIsAlreadyExistError
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.viewsets import ViewSet             #for upload
from rest_framework.response import Response            #
from Kemsu_Document.serializers import FileSerializer #

from Kemsu_Document.models import (
    User, Department, Group, Institute,
    Module, Point, Student,Statement
)
from django.conf import settings
from djangoProject.forms import DocumentForm

from Kemsu_Document.serializers import (
    RegistrationStudentSerializer, RegistrationStaffSerializer,
    GroupSerializer,
    InstituteSerializer, ModuleSerializer,
    PointSerializer, BypassSheetsSerializer, PostByPassSheetsSerializer,
    GetByPassSheetsDetailSerializer, TokenEmailPairSerializer,
    TokenUsernamePairSerializer, UpdateUserSerializer, StudentSerializer,
    RefreshTokenSerializer, DepartmentsSerializer, )
from . import settings


class RegistrationStudentAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationStudentSerializer

    def post(self, request):
        tokenr = RefreshToken()
        tokena = AccessToken().for_user(request.user)

        serializer = RegistrationStudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except GroupNotFoundError:
            return Response(
                {
                    "message": "This group does not exist"
                },
                status=status.HTTP_200_OK
            )
        except ThisUserIsAlreadyExistException:
            return Response(
                {
                    "message": "A user with this full name already exists. Please enter your record book number"
                },
                status=status.HTTP_200_OK
            )
        except ThisEmailIsAlreadyExistError:
            return Response(
                {
                    "message": "This email is already exist"
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'accessToken': str(tokena),
                'refreshToken': str(tokenr),
                'expiresIn': settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].seconds
            },
            status=status.HTTP_201_CREATED,
        )


class RegistrationStaffAPIView(APIView):
    permission_classes = [AllowAny]

    serializer_class = RegistrationStaffSerializer

    def post(self, request):
        # tokenr = TokenObtainPairSerializer().get_token(request.user)
        # tokena = AccessToken().for_user(request.user)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                # 'accessToken': str(tokena),
                # 'refreshToken': str(tokenr),
                'expiresIn': settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].seconds
            },
            status=status.HTTP_201_CREATED,
        )


class GroupList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        group = Group.objects.all()
        serializer = GroupSerializer(group, many=True)

        return Response(serializer.data)


class InstituteList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        institute = Institute.objects.all()
        serializer = InstituteSerializer(institute, many=True)

        return Response(serializer.data)


class ModuleList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        module = Module.objects.all()
        serializer = ModuleSerializer(module, many=True)

        return Response(serializer.data)


class PointList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        point = Point.objects.all()
        serializer = PointSerializer(point, many=True)

        return Response(serializer.data)


class StudentList(APIView):
    # permission_classes = [IsAdminUser]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        student = Student.objects.get(user=pk)
        serializer = StudentSerializer(student)

        return Response(serializer.data)

    def patch(self, request, pk):
        user = User.objects.get(id=pk)
        serializer = UpdateUserSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def test_func(self):
    #     obj = self.get_object()
    #     return obj == self.request.user


class BypassSheetsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        module = Module.objects.all()
        serializer = BypassSheetsSerializer(module, many=True)

        return Response(serializer.data)


class PostByPassSheetsView(APIView):
    permission_classes = [IsAuthenticated]

    def create_points(self, pk):
        point = Point()
        module = Module.objects.get(id=pk)
        point.create_module('Отдел1', 'Описание1', module)
        point2 = Point()
        point2.create_module('Отдел2', 'Описание2', module)
        point3 = Point()
        point3.create_module('Отдел3', 'Описание3', module)
        point4 = Point()
        point4.create_module('Отдел4', 'Описание4', module)
        point5 = Point()
        point5.create_module('Отдел5', 'Описание5', module)

    def post(self, request, pk):
        request.data.update({"student_id": pk})
        serializer = PostByPassSheetsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.create_points(serializer.data["id"])
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetByPassSheetsDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        point = Point.objects.filter(module_id=pk)
        serializer = GetByPassSheetsDetailSerializer(point, many=True)

        return Response(serializer.data)


class TokenEmailPairView(TokenObtainPairView):
    serializer_class = TokenEmailPairSerializer


class TokenUsernamePairView(TokenObtainPairView):
    serializer_class = TokenUsernamePairSerializer


class LogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DepartmentsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        departments = Department.objects.all()
        serializer_class = DepartmentsSerializer(departments, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def get(self, request, institute):
        institute = Institute.objects.get(title=institute)
        departments = Department.objects.filter(institute=institute.id)
        departments |= Department.objects.filter(institute=None)
        serializer_class = DepartmentsSerializer(departments, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)


class FileView (APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post (self, request, *args, **kwargs):
        file_serializer = FileSerializer (data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
