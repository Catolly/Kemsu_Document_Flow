
from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from Kemsu_Document.exceptions import GroupNotFoundError, ThisUserIsAlreadyExistException, ThisEmailIsAlreadyExistError, \
    DepartmentNotFoundException
from Kemsu_Document.models import (
    User, Module,
    Point, Student,
)

from Kemsu_Document.serializers import (
    RegistrationStudentSerializer, RegistrationStaffSerializer,
    BypassSheetsSerializer, TokenEmailPairSerializer,
    UpdateUserSerializer, StudentSerializer,
    LogoutSerializer, RefreshTokenSerializer, PostByPassSheetsSerializer, LoginSerializer,
)

from .permissions import (IsAdmin, IsStudent, IsStaff,
                          StudentListViewPermission, PatchUserDataPermission, BypassSheetsViewPermission, )


class RegistrationStudentAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

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
    permission_classes = (permissions.AllowAny,)

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

    def get(self, request, pk):
        self.permission_classes = [StudentListViewPermission]
        student = Student.objects.get(user=pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def patch(self, request, pk):
        self.permission_classes = [PatchUserDataPermission]
        user = User.objects.get(id=pk)
        serializer = UpdateUserSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BypassSheetsView(APIView):

    #permission_classes = [BypassSheetsViewPermission]

    def get(self, request):
        self.permission_classes = [IsAuthenticated]
        if request.user.status == "Студент":
            modules = Module.objects.filter(student_id=request.user.id)
        else:
            modules = Module.objects.all()
        serializer = BypassSheetsSerializer(modules, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        self.permission_classes = [BypassSheetsViewPermission]
        serializer = PostByPassSheetsSerializer(data=request.data, context={"request" : request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

class BypassSheetView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        if request.user.status == "Студент":
            module = Module.objects.filter(id=pk, student_id=request.user.id).first()
        elif request.user.status == "Работник" or request.user.status == "Администратор":
            module = Module.objects.filter(id=pk).first()
        else:
            return Response(
                {
                    "message": "You don't have permissions to perform this action"
                },
                status=status.HTTP_409_CONFLICT)

        serializer = BypassSheetsSerializer(module)

        return Response(serializer.data, status=status.HTTP_200_OK)

class LoginView(TokenObtainPairView):
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
    serializer_class = RefreshTokenSerializer