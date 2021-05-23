from datetime import time, datetime
from django.db.models import QuerySet
from rest_framework import status, permissions, viewsets
from rest_framework.generics import GenericAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.core.mail import send_mail

from Kemsu_Document.exceptions import GroupNotFoundError, ThisUserIsAlreadyExistException, ThisEmailIsAlreadyExistError, \
    DepartmentNotFoundException, BypassSheetTemplateExistException
from Kemsu_Document.models import (
    User, BypassSheet,
    Point, Student, Department, Institute, Group, BypassSheetTemplate, Staff, Statement, RequiredDocuments,
    StatementsTemplate, PointTemplate, RequiredDocumentsTemplate, UploadDocumentsFormat
)

from Kemsu_Document.serializers import (
    RegistrationStudentSerializer, RegistrationStaffSerializer,
    BypassSheetsSerializer, TokenEmailPairSerializer,
    UpdateUserSerializer, StudentSerializer,
    LogoutSerializer, RefreshTokenSerializer, PostByPassSheetsSerializer, DepartmentsSerializer, FileSerializer,
    GroupSerializer, PostBypassSheetTemplateSerializer, BypassSheetTemplateSerializer, UnregisteredStudentSerializer,
    CheckAccessSerializer, UserBypassSheetSerializer, UserBypassSheetPointSerializer,
    StaffSerializer, UploadDocumentsSerializer, SigningPointSerializer, UpdateBypassSheetTemplateSerializer,
    BypassSheetTemplateTitleSerializer
)

from .permissions import (
    BypassSheetsViewPermission, UsersViewPermission, BypassSheetViewPermission,
    UserViewPermission, BanUnbanPermission, UploadDocumentsPermission, DepartmentViewPermission, GroupViewPermission,
    BypassSheetTemplateViewPermission, )
from .service import Pagination


class RegistrationStudentAPIView(APIView):
    permission_classes = [AllowAny]

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
                status=status.HTTP_400_BAD_REQUEST
            )
        except ThisUserIsAlreadyExistException:
            return Response(
                {
                    "message": "A user with this full name already exists. Please enter your record book number"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except ThisEmailIsAlreadyExistError:
            return Response(
                {
                    "message": "This email is already exist"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        data.update(serializer.data)
        data.update(serializer.validated_data)
        return Response(
            data,
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
                status=status.HTTP_400_BAD_REQUEST
            )
        except ThisUserIsAlreadyExistException:
            return Response(
                {
                    "message": "A user with this full name already exists."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except ThisEmailIsAlreadyExistError:
            return Response(
                {
                    "message": "This email is already exist"
                },
                status=status.HTTP_400_BAD_REQUEST
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

class BypassSheetsView(APIView):
    permission_classes = [BypassSheetsViewPermission]
    serializer_class = PostByPassSheetsSerializer

    # permission_classes = [AllowAny]

    def get(self, request):
        if request.user.status == "Студент":
            bypass_sheet = BypassSheet.objects.filter(student_id=request.user.id)
        else:
            bypass_sheet = BypassSheet.objects.all()
        serializer = BypassSheetsSerializer(bypass_sheet, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):

        user = request.user

        department_name = request.GET.get('department', '')

        serializer = SigningPointSerializer(data=request.data,
                                            context={
                                                'department_name':department_name,
                                                'user': user,
                                            }, many=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(status=status.HTTP_200_OK)

class BypassSheetView(APIView):

    permission_classes = [UploadDocumentsPermission]
    # permission_classes = [AllowAny]

    def get_queryset(self):
        bypass_sheet = BypassSheet.objects.filter(id=self.kwargs['pk']).first()

        return Point.objects.filter(bypass_sheet=bypass_sheet, title=self.request.data['title'])

    def patch(self, request, *args, **kwargs):
        serializer = UploadDocumentsSerializer(data=request.data,
                                                 context={'id': self.kwargs['pk']})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(status=status.HTTP_200_OK)


class LoginView(TokenObtainPairView):
    serializer_class = TokenEmailPairSerializer

class LogoutView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RefreshTokenView(TokenRefreshView):
    serializer_class = RefreshTokenSerializer

class DepartmentsView(APIView):

    # permission_classes = [DepartmentViewPermission]

    permission_classes = [AllowAny]

    def get(self, request):
        institute_title = request.GET.get('institute', '')

        if institute_title == "":
            departments = Department.objects.all()
            serializer = DepartmentsSerializer(departments, many=True)
        else:
            institute = Institute.objects.filter(title=institute_title).first()

            department_title = request.GET.get('department', '')

            if department_title == "":
                department = Department.objects.filter(institute=institute)
            else:
                department = Department.objects.filter(title=department_title, institute=institute)
            serializer = DepartmentsSerializer(department, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GroupApiView(APIView):
    permission_classes = [GroupViewPermission]

    serializer_class = GroupSerializer

    def get(self, request):
        group = Group.objects.all()

        serializer = self.serializer_class(group, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class BypassSheetsTemplateApiView(APIView):
    permission_classes = [BypassSheetTemplateViewPermission]

    def get(self, request):
        bypass_sheets_templates = BypassSheetTemplate.objects.all()

        serializer = BypassSheetTemplateSerializer(bypass_sheets_templates, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PostBypassSheetTemplateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except BypassSheetTemplateExistException:
            return Response({
                'message' : 'Такой обходной лист уже существует'
            }, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_201_CREATED)

class BypassSheetTemplateApiView(APIView):
    permission_classes = [BypassSheetTemplateViewPermission]

    # permission_classes = [AllowAny]

    def get(self, request, pk):
        bypass_sheet_template = BypassSheetTemplate.objects.filter(id=pk).first()

        serializer = BypassSheetTemplateSerializer(bypass_sheet_template)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        return BypassSheetTemplate.objects.get(id=self.kwargs['pk'])

    def patch(self, request, pk):

        data = request.data

        serializer = UpdateBypassSheetTemplateSerializer(data=request.data,
                                                         context={
                                                             'id': pk
                                                         })

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk):

        BypassSheetTemplate.objects.get(id=pk).delete()

        return Response(status=status.HTTP_200_OK)

class UnregisteredStudentListApiView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    pagination_class = Pagination

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        institute_title = self.request.GET.get('institute', '')
        course = self.request.GET.get('course', '')
        group_title = self.request.GET.get('group', '')

        if institute_title != "" and course == "" and group_title == "":

            students = Student.objects.filter(user=None)

            institute = Institute.objects.get(title=institute_title)

            groups = Group.objects.filter(institute=institute)

            for group in groups:
                students |= Student.objects.filter(group=group)

            new_student_query = Student.objects.filter(user=None)

            users = User.objects.filter(id=None)

            if search != "":
                for student in students:
                    if search.upper() in student.user.fullname.upper():
                        new_student_query |= Student.objects.filter(user=student.user)

                for student in new_student_query:
                    if student.user.is_active == False:
                        users |= User.objects.filter(id=student.user.id)
                return users

            for student in students:
                if student.user.is_active == False:
                    users |= User.objects.filter(id=student.user.id)
            return users

        elif institute_title == "" and course != "" and group_title == "":

            students = Student.objects.filter(user=None)

            all_groups = Group.objects.all()
            required_groups = Group.objects.filter(id=None)

            for group in all_groups:
                recruitment_data = group.recruitment_date

                course_number = int(((datetime.now().date() - recruitment_data).days) // 365.2425) + 1

                if course_number == int(course):
                    required_groups |= Group.objects.filter(id=group.id)

            for group in required_groups:
                students |= Student.objects.filter(group=group)

            new_student_query = Student.objects.filter(user=None)

            users = User.objects.filter(id=None)

            if search != "":
                for student in students:
                    if search.upper() in student.user.fullname.upper():
                        new_student_query |= Student.objects.filter(user=student.user)

                for student in new_student_query:
                    if student.user.is_active == False:
                        users |= User.objects.filter(id=student.user.id)
                return users

            for student in students:
                if student.user.is_active == False:
                    users |= User.objects.filter(id=student.user.id)
            return users

        elif institute_title == "" and course == "" and group_title != "":

            students = Student.objects.filter(user=None)

            groups = Group.objects.filter(name=group_title)

            for group in groups:
                students |= Student.objects.filter(group=group)

            new_student_query = Student.objects.filter(user=None)

            users = User.objects.filter(id=None)

            if search != "":
                for student in students:
                    if search.upper() in student.user.fullname.upper():
                        new_student_query |= Student.objects.filter(user=student.user)

                for student in new_student_query:
                    if student.user.is_active == False:
                        users |= User.objects.filter(id=student.user.id)
                return users

            for student in students:
                if student.user.is_active == False:
                    users |= User.objects.filter(id=student.user.id)
            return users

        elif institute_title != "" and course != "" and group_title == "":

            students = Student.objects.filter(user=None)

            institute = Institute.objects.get(title=institute_title)

            all_groups = Group.objects.filter(institute=institute)

            required_groups = Group.objects.filter(id=None)

            for group in all_groups:
                recruitment_data = group.recruitment_date

                course_number = int(((datetime.now().date() - recruitment_data).days) // 365.2425) + 1

                if course_number == int(course):
                    required_groups |= Group.objects.filter(id=group.id)

            for group in required_groups:
                students |= Student.objects.filter(group=group)

            new_student_query = Student.objects.filter(user=None)

            users = User.objects.filter(id=None)

            if search != "":
                for student in students:
                    if search.upper() in student.user.fullname.upper():
                        new_student_query |= Student.objects.filter(user=student.user)

                for student in new_student_query:
                    if student.user.is_active == False:
                        users |= User.objects.filter(id=student.user.id)
                return users

            for student in students:
                if student.user.is_active == False:
                    users |= User.objects.filter(id=student.user.id)
            return users

        elif ((institute_title != "" and course == "" and group_title != "")
              or (institute_title != "" and course != "" and group_title != "")):

            institute = Institute.objects.get(title=institute_title)

            group = Group.objects.get(institute=institute, name=group_title)

            students = Student.objects.filter(group=group)

            new_student_query = Student.objects.filter(user=None)

            users = User.objects.filter(id=None)

            if search != "":
                for student in students:
                    if search.upper() in student.user.fullname.upper():
                        new_student_query |= Student.objects.filter(user=student.user)

                for student in new_student_query:
                    if student.user.is_active == False:
                        users |= User.objects.filter(id=student.user.id)
                return users

            for student in students:
                if student.user.is_active == False:
                    users |= User.objects.filter(id=student.user.id)
            return users

        elif institute_title == "" and course != "" and group_title != "":

            students = Student.objects.filter(user=None)

            all_groups = Group.objects.filter(name=group_title)

            required_groups = Group.objects.filter(id=None)

            for group in all_groups:
                recruitment_data = group.recruitment_date

                course_number = int(((datetime.now().date() - recruitment_data).days) // 365.2425) + 1

                if course_number == int(course):
                    required_groups |= Group.objects.filter(id=group.id)

            for group in required_groups:
                students |= Student.objects.filter(group=group)

            new_student_query = Student.objects.filter(user=None)

            users = User.objects.filter(id=None)

            if search != "":
                for student in students:
                    if search.upper() in student.user.fullname.upper():
                        new_student_query |= Student.objects.filter(user=student.user)

                for student in new_student_query:
                    if student.user.is_active == False:
                        users |= User.objects.filter(id=student.user.id)
                return users

            for student in students:
                if student.user.is_active == False:
                    users |= User.objects.filter(id=student.user.id)
            return users

        elif institute_title == "" and course == "" and group_title == "" and search != "":
            students = Student.objects.all()

            new_student_query = Student.objects.filter(user=None)

            users = User.objects.filter(id=None)

            if search != "":
                for student in students:
                    if search.upper() in student.user.fullname.upper():
                        new_student_query |= Student.objects.filter(user=student.user)

                for student in new_student_query:
                    if student.user.is_active == False:
                        users |= User.objects.filter(id=student.user.id)
                return users

            for student in students:
                if student.user.is_active == False:
                    users |= User.objects.filter(id=student.user.id)
            return users

        else:
            return User.objects.filter(status='Студент', is_active=False)

    def get_serializer_class(self):

        if self.action == "list":
            return UnregisteredStudentSerializer

    def list(self, request, *args, **kwargs):
        if request.GET.get('limit', '') != '':

            page = self.paginate_queryset(self.get_queryset())
            serializer = self.get_serializer(page, many=True)

            return self.get_paginated_response(
                {'studentsAmount': len(self.get_queryset()), 'students': serializer.data})

        serializer = self.get_serializer(self.get_queryset(), many=True)

        return Response({'studentsAmount': len(serializer.data), 'students': serializer.data}, status.HTTP_200_OK)

class CheckAccessApiView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CheckAccessSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class UsersListView(viewsets.ReadOnlyModelViewSet):
    # permission_classes = [UsersViewPermission]
    permission_classes = [AllowAny]
    pagination_class = Pagination

    def get_serializer_context(self):
        if self.request.GET.get('title', '') == "":
            return {}

        if self.request.GET.get('pointTitle', '') == "":
            return {
                'bypassSheetsName': self.request.GET.get('title', '')
            }
        else:
            return {
                'bypassSheetsName': self.request.GET.get('title', ''),
                'pointName': self.request.GET.get('pointTitle', '')
            }

    def __getBypassSheetQuery(self):
        self.bypassSheets = BypassSheet.objects.filter(title=None)

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

    def get_queryset(self):
        self.bypassSheetsName = self.request.GET.get('title', '')
        self.pointName = self.request.GET.get('pointTitle', '')

        search = self.request.GET.get('search', '')
        institute_title = self.request.GET.get('institute', '')
        course = self.request.GET.get('course', '')
        group_title = self.request.GET.get('group', '')

        self.bypassSheets = BypassSheet.objects.filter(title=self.bypassSheetsName)

        if institute_title != "" and course == "" and group_title == "":

            students = Student.objects.filter(user=None)

            institute = Institute.objects.get(title=institute_title)

            groups = Group.objects.filter(institute=institute)

            for group in groups:

                students |= Student.objects.filter(group=group)

            new_student_query = Student.objects.filter(user=None)

            if search != "":
                for student in students:
                    if search.upper() in student.user.fullname.upper():
                        new_student_query |= Student.objects.filter(user=student.user)

                return new_student_query

            return students

        elif institute_title == "" and course != "" and group_title == "":

            students = Student.objects.filter(user=None)

            all_groups = Group.objects.all()
            required_groups = Group.objects.filter(id=None)

            for group in all_groups:
                recruitment_data = group.recruitment_date

                course_number = int(((datetime.now().date() - recruitment_data).days) // 365.2425) + 1

                if course_number == int(course):
                    required_groups |= Group.objects.filter(id=group.id)

            for group in required_groups:
                students |= Student.objects.filter(group=group)

            new_student_query = Student.objects.filter(user=None)

            if search != "":
                for student in students:
                    if search.upper() in student.user.fullname.upper():
                        new_student_query |= Student.objects.filter(user=student.user)

                return new_student_query

            return students

        elif institute_title == "" and course == "" and group_title != "":

            students = Student.objects.filter(user=None)

            groups = Group.objects.filter(name=group_title)

            for group in groups:
                students |= Student.objects.filter(group=group)

            new_student_query = Student.objects.filter(user=None)

            if search != "":
                for student in students:
                    if search.upper() in student.user.fullname.upper():
                        new_student_query |= Student.objects.filter(user=student.user)

                return new_student_query

            return students

        elif institute_title != "" and course != "" and group_title == "":

            students = Student.objects.filter(user=None)

            institute = Institute.objects.get(title=institute_title)

            all_groups = Group.objects.filter(institute=institute)

            required_groups = Group.objects.filter(id=None)

            for group in all_groups:
                recruitment_data = group.recruitment_date

                course_number = int(((datetime.now().date() - recruitment_data).days) // 365.2425) + 1

                if course_number == int(course):
                    required_groups |= Group.objects.filter(id=group.id)

            for group in required_groups:
                students |= Student.objects.filter(group=group)

            new_student_query = Student.objects.filter(user=None)

            if search != "":
                for student in students:
                    if search.upper() in student.user.fullname.upper():
                        new_student_query |= Student.objects.filter(user=student.user)

                return new_student_query

            return students

        elif((institute_title != "" and course == "" and group_title != "")
             or (institute_title != "" and course != "" and group_title != "")):

            institute = Institute.objects.get(title=institute_title)

            group = Group.objects.get(institute=institute, name=group_title)

            students = Student.objects.filter(group=group)

            new_student_query = Student.objects.filter(user=None)

            if search != "":
                for student in students:
                    if search.upper() in student.user.fullname.upper():
                        new_student_query |= Student.objects.filter(user=student.user)

                return new_student_query

            return students

        elif institute_title == "" and course != "" and group_title != "":

            students = Student.objects.filter(user=None)

            all_groups = Group.objects.filter(name=group_title)

            required_groups = Group.objects.filter(id=None)

            for group in all_groups:
                recruitment_data = group.recruitment_date

                course_number = int(((datetime.now().date() - recruitment_data).days) // 365.2425) + 1

                if course_number == int(course):
                    required_groups |= Group.objects.filter(id=group.id)

            for group in required_groups:
                students |= Student.objects.filter(group=group)

            new_student_query = Student.objects.filter(user=None)

            if search != "":
                for student in students:
                    if search.upper() in student.user.fullname.upper():
                        new_student_query |= Student.objects.filter(user=student.user)

                return new_student_query

            return students

        elif institute_title == "" and course == "" and group_title == "" and search != "":
            students = Student.objects.all()

            new_student_query = Student.objects.filter(user=None)

            if search != "":
                for student in students:
                    if search.upper() in student.user.fullname.upper():
                        new_student_query |= Student.objects.filter(user=student.user)

                return new_student_query

            return students

        if self.bypassSheetsName == "":
            return Student.objects.all()

        if self.pointName == "":
            return self.__getUserBypassSheetQuery()
        else:
            self.points = Point.objects.filter(title=self.pointName)
            return self.__getUserPointQuery()

    def get_serializer_class(self):

        if self.action == "list":
            if self.request.GET.get('title', '') == "":
                return StudentSerializer
            if self.request.GET.get('pointTitle', '') == "":
                return UserBypassSheetSerializer
            else:
                return UserBypassSheetPointSerializer

    def list(self, request, *args, **kwargs):
        if request.GET.get('limit', '') != '':
            page = self.paginate_queryset(self.get_queryset())
            serializer = self.get_serializer(page, context=self.get_serializer_context(), many=True)

            return self.get_paginated_response({'studentsAmount':len(self.get_queryset()), 'students':serializer.data})

        serializer = self.get_serializer(self.get_queryset(), context=self.get_serializer_context(), many=True)

        return Response({'studentsAmount':len(serializer.data), 'students':serializer.data}, status.HTTP_200_OK)

class BanApiView(APIView):
    permission_classes = [BanUnbanPermission]

    def post(self, request, pk):

        user = User.objects.filter(id=pk).first()

        user.is_baned = True

        user.save()

        return Response(status=status.HTTP_200_OK)

class UnbanApiView(APIView):
    permission_classes = [BanUnbanPermission]

    def post(self, request, pk):

        user = User.objects.filter(id=pk).first()

        user.is_baned = False

        user.save()

        return Response(status=status.HTTP_200_OK)

class BypassSheetTemplateTitle(APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self, education_form):
        return BypassSheetTemplate.objects.filter(educationForm=education_form)

    def get(self, request):

        education_form = request.GET.get('educationForm')

        serializer = BypassSheetTemplateTitleSerializer(self.get_queryset(education_form), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)