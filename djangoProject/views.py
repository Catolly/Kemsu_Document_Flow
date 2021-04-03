
from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from Kemsu_Document.exceptions import GroupNotFoundError, ThisUserIsAlreadyExistException, ThisEmailIsAlreadyExistError, \
    DepartmentNotFoundException
from Kemsu_Document.models import (
    User, Group, Institute,
    Module, Point, Student,
)

from Kemsu_Document.serializers import (
    RegistrationStudentSerializer, RegistrationStaffSerializer,
    BypassSheetsSerializer, TokenEmailPairSerializer,
    UpdateUserSerializer, StudentSerializer,
    LogoutSerializer, RefreshTokenSerializer,
)

from .permissions import PermissionIsStaff


class RegistrationStudentAPIView(APIView):
    permission_classes = [AllowAny]

    serializer_class = RegistrationStudentSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except GroupNotFoundError:
            return Response(
                {
                    "message": "This group does not exist"
                },
                status=status.HTTP_409_CONFLICT
            )
        except ThisUserIsAlreadyExistException:
            return Response(
                {
                    "message": "A user with this full name already exists. Please enter your record book number"
                },
                status=status.HTTP_409_CONFLICT
            )
        except ThisEmailIsAlreadyExistError:
            return Response(
                {
                    "message": "This email is already exist"
                },
                status=status.HTTP_409_CONFLICT
            )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

class RegistrationStaffAPIView(APIView):
    permission_classes = [AllowAny]

    serializer_class = RegistrationStaffSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except DepartmentNotFoundException:
            return Response(
                {
                    "message": "This department does not exist"
                },
                status=status.HTTP_409_CONFLICT
            )
        except ThisUserIsAlreadyExistException:
            return Response(
                {
                    "message": "A user with this full name already exists."
                },
                status=status.HTTP_409_CONFLICT
            )
        except ThisEmailIsAlreadyExistError:
            return Response(
                {
                    "message": "This email is already exist"
                },
                status=status.HTTP_409_CONFLICT
            )
        return Response(
            {
                "message" : "Registration request has been sent to the administrator"
            },
            status=status.HTTP_201_CREATED
        )

class StudentList(APIView):
    permission_classes = [PermissionIsStaff]

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

class BypassSheetsView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        module = Module.objects.all()
        serializer = BypassSheetsSerializer(module, many=True)

        return Response(serializer.data)

# class PostByPassSheetsView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def create_points(self, pk):
#         point = Point()
#         module = Module.objects.get(id=pk)
#         point.create_module('Отдел1', 'Описание1', module)
#         point2 = Point()
#         point2.create_module('Отдел2', 'Описание2', module)
#         point3 = Point()
#         point3.create_module('Отдел3', 'Описание3', module)
#         point4 = Point()
#         point4.create_module('Отдел4', 'Описание4', module)
#         point5 = Point()
#         point5.create_module('Отдел5', 'Описание5', module)
#
#
#     def post(self, request, pk):
#         request.data.update({"student_id" : pk})
#         serializer = PostByPassSheetsSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         self.create_points(serializer.data["id"])
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

class TokenEmailPairView(TokenObtainPairView):
    serializer_class = TokenEmailPairSerializer

class LogoutView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RefreshTokenView(TokenRefreshView):
    # serializer_class = RefreshTokenSerializer
    # #permission_classes = (permissions.IsAuthenticated, )
    # permission_classes = [AllowAny]
    #
    # def post(self, request, *args):
    #     sz = self.get_serializer(data=request.data)
    #     sz.is_valid(raise_exception=True)
    #     sz.save()
    #     return Response(sz.data, status=status.HTTP_204_NO_CONTENT)
    serializer_class = RefreshTokenSerializer