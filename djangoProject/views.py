from django.db.models import QuerySet, Q
from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from Kemsu_Document.exceptions import GroupNotFoundError, ThisUserIsAlreadyExistException, ThisEmailIsAlreadyExistError, \
    DepartmentNotFoundException
from Kemsu_Document.models import (
    User, BypassSheet,
    Point, Student, Department, Institute, Group, BypassSheetTemplate, Staff, Statement,
)

from Kemsu_Document.serializers import (
    RegistrationStudentSerializer, RegistrationStaffSerializer,
    BypassSheetsSerializer, TokenEmailPairSerializer,
    UpdateUserSerializer, StudentSerializer,
    LogoutSerializer, RefreshTokenSerializer, PostByPassSheetsSerializer, DepartmentsSerializer,
    UserBypassSheetSerializer, FileSerializer, GroupSerializer, BypassSheetTemplateSerializer,
    PostBypassSheetTemplateSerializer, UnregisteredStudentSerializer, CheckAccessSerializer,
    UserBypassSheetPointSerializer, StaffSerializer, UpdateBypassSheetSerializer,
)

from .permissions import (
    BypassSheetsViewPermission, UsersViewPermission, BypassSheetViewPermission,
    UserViewPermission, )


class RegistrationStudentAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    serializer_class = RegistrationStudentSerializer

    def post(self, request):

        data = dict()

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
        data.update(serializer.data)
        data.update(serializer.validated_data)
        return Response(
            data,
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

class UserList(APIView):
    permission_classes = [UserViewPermission]

    def get(self, request, pk):
        student = Student.objects.filter(user=pk).first()

        if not student:
            staff = Staff.objects.filter(user=pk).first()
            if not staff:
                return Response(
                    {
                        "message": "The user with this id does not exist"
                    },
                    status=status.HTTP_204_NO_CONTENT
                )
            serializer = StaffSerializer(staff)
        else:
            serializer = StudentSerializer(student)
        return Response(serializer.data)

    def patch(self, request, pk):
        user = User.objects.filter(id=pk).first()
        serializer = UpdateUserSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UsersListView(APIView):
    # permission_classes = [UsersViewPermission]
    permission_classes = [AllowAny]

    def get(self, request):
        student = Student.objects.all()

        serializer = StudentSerializer(student, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class BypassSheetsView(APIView):

    permission_classes = [BypassSheetsViewPermission]
    serializer_class = PostByPassSheetsSerializer

    def get(self, request):
        if request.user.status == "Студент":
            bypass_sheet = BypassSheet.objects.filter(student_id=request.user.id)
        elif request.user.status == "Работник":
            bypass_sheet = BypassSheet.objects.all()
        else:
            bypass_sheet = BypassSheet.objects.all()
        serializer = BypassSheetsSerializer(bypass_sheet, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request" : request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

class BypassSheetView(APIView):
    # parser_classes = (MultiPartParser, FormParser)
    # permission_classes = [BypassSheetViewPermission]
    permission_classes = [AllowAny]

    def __updateStatements(self, bypass_sheet, statements_data):

        for statement_data in statements_data:

            obj, statement = Statement.objects.update_or_create(title=statement_data['title'], bypass_sheet=bypass_sheet,
                                                           defaults = {
                                                               'title': statement_data.get('title'),
                                                               'file': statement_data.get('file')
                                                           })

    def patch(self, request, pk):
        data = request.data

        bypass_sheet = BypassSheet.objects.filter(id=pk).first()

        bypass_sheet.title = data.get('title', bypass_sheet.title)

        bypass_sheet.save()

        self.__updateStatements(bypass_sheet, data['statements'])

        serializer = BypassSheetsSerializer(bypass_sheet)

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

class DepartmentsView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        departments = Department.objects.all()
        serializer_class = DepartmentsSerializer(departments, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

class DepartmentInstituteView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, institute):
        institute = Institute.objects.filter(title=institute).first()
        departments = Department.objects.filter(institute=institute.id)
        departments |= Department.objects.filter(institute=None)
        serializer_class = DepartmentsSerializer(departments, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

class UserBypassSheetsView(APIView):

    permission_classes = [AllowAny]

    def __getBypassSheetQuery(self):
        self.bypassSheets = BypassSheet.objects.filter(name=None)

        for point in self.points:
            self.bypassSheets |= BypassSheet.objects.filter(id=point.bypass_sheet.id)

    def __getUserBypassSheetQuery(self):

        userQuery = Student.objects.filter(user=None)

        for bypassSheet in self.bypassSheets:
            userQuery |= Student.objects.filter(user=bypassSheet.student_id.user)

        return userQuery

    def __getUserPointQuery(self):

        userQuery = Student.objects.filter(user=None)

        self.__getBypassSheetQuery()

        for bypassSheet in self.bypassSheets:
            userQuery |= Student.objects.filter(user=bypassSheet.student_id.user)

        return userQuery

    def get(self, request):
        bypassSheetsName = request.GET.get('name', '')
        pointName = request.GET.get('pointName', '')

        self.bypassSheets = BypassSheet.objects.filter(name=bypassSheetsName)

        if pointName == "":
            students = self.__getUserBypassSheetQuery()
            serializer = UserBypassSheetSerializer(students, context={'bypassSheetsName': bypassSheetsName}, many=True)
        else:
            self.points = Point.objects.filter(title=pointName)
            students = self.__getUserPointQuery()
            serializer = UserBypassSheetPointSerializer(students, context={'bypassSheetsName': bypassSheetsName,
                                                                           'pointName' : pointName}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FileApiView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny]
    serializer_class = FileSerializer

    def post(self, request):
        file_serializer = self.serializer_class(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupApiView(APIView):
    permission_classes = [AllowAny]

    serializer_class = GroupSerializer

    def get(self, request):
        group = Group.objects.all()

        serializer = self.serializer_class(group, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class BypassSheetsTemplateApiView(ListCreateAPIView):
    permission_classes = [AllowAny]

    queryset = BypassSheetTemplate.objects.all()

    serializer_class = PostBypassSheetTemplateSerializer

    def get(self, request):
        bypass_sheets_templates = BypassSheetTemplate.objects.all()

        serializer = BypassSheetTemplateSerializer(bypass_sheets_templates, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        # else:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)

class BypassSheetTemplateApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        bypass_sheet_template = BypassSheetTemplate.objects.filter(id=pk).first()

        serializer = BypassSheetTemplateSerializer(bypass_sheet_template)

        return Response(serializer.data, status=status.HTTP_200_OK)

class UnregisteredStudentListApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        unregistered_student_query_set = User.objects.filter(status='Студент', is_active=False)

        serializer = UnregisteredStudentSerializer(unregistered_student_query_set, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class CheckAccessApiView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CheckAccessSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.validated_data, status=status.HTTP_200_OK)