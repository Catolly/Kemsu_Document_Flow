from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from Kemsu_Document.models import (
    User, Department, Group, Institute,
    Module, Point, Staff, Student,
)

from Kemsu_Document.serializers import (LoginSerializer,
                                        RegistrationStudentSerializer, RegistrationStaffSerializer,
                                        DepartmentSerializer, GroupSerializer,
                                        InstituteSerializer, ModuleSerializer,
                                        PointSerializer, StaffSerializer,
                                        StudentSerializer, UserSerializer,
                                        GetBypassSheetsSerializer, PostByPassSheetsSerializer,
                                        GetByPassSheetsDetailSerializer, TokenEmailPairSerializer,
                                        TokenUsernamePairSerializer,
                                        )

from .permissions import IsStudentUser

class RegistrationStudentAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationStudentSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                'message': 'Registration is success',
                    #serializer.data.get('token', None),
            },
            status=status.HTTP_201_CREATED,
        )

class RegistrationStaffAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationStaffSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                'message': 'Registration is success'
                # 'token': serializer.data.get('token', None),
            },
            status=status.HTTP_201_CREATED,
        )

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class DepartmentList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        department = Department.objects.all()
        serializer = DepartmentSerializer(department, many=True)

        return Response(serializer.data)

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

class StaffList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        staff = Staff.objects.all()
        serializer = StaffSerializer(staff, many=True)

        return Response(serializer.data)


class StudentList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)

        return Response(serializer.data)


class UserList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)

        return Response(serializer.data)

class GetBypassSheetsView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        module = Module.objects.filter(student_id=pk)
        serializer = GetBypassSheetsSerializer(module, many=True)

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
        request.data.update({"student_id" : pk})
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