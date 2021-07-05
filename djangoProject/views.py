import openpyxl
import time

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
    StatementsTemplate, PointTemplate, RequiredDocumentsTemplate, UploadDocumentsFormat, UploadedDocuments
)

from Kemsu_Document.serializers import (
    RegistrationStudentSerializer, RegistrationStaffSerializer,
    BypassSheetsSerializer, TokenEmailPairSerializer,
    UpdateUserSerializer, StudentSerializer,
    LogoutSerializer, RefreshTokenSerializer, PostByPassSheetsSerializer, DepartmentsSerializer, FileSerializer,
    GroupSerializer, PostBypassSheetTemplateSerializer, BypassSheetTemplateSerializer, UnregisteredStudentSerializer,
    CheckAccessSerializer, UserBypassSheetSerializer, UserBypassSheetPointSerializer,
    StaffSerializer, UploadDocumentsSerializer, SigningPointSerializer, UpdateBypassSheetTemplateSerializer,
    BypassSheetTemplateTitleSerializer, StudentTestSerializer, GetBypassSheetsSchemaDeadlinesSerializer,
    PatchBypassSheetsSchemaDeadlinesSerializer
)

from .permissions import (
    BypassSheetsViewPermission, UsersViewPermission, BypassSheetViewPermission,
    UserViewPermission, BanUnbanPermission, UploadDocumentsPermission, DepartmentViewPermission, GroupViewPermission,
    BypassSheetTemplateViewPermission, UploadStudentsPermission, UpdateBypassSheetSchemaDeadline, GetBypassSheetsSchemaDeadline )
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

        if search != "":

            students = Student.objects.all().select_related('user')

            new_student_query = Student.objects.filter(user=None)

            users = User.objects.filter(id=None)

            for student in students:
                if ((search.upper() in student.user.fullname.upper()) and (student.user.is_active == False)):
                    new_student_query |= Student.objects.filter(user=student.user)

            for student in new_student_query:
                    users |= User.objects.filter(id=student.user.id)
            return users.order_by('fullname')
        else:
            return User.objects.filter(status='Студент', is_active=False).select_related('student').order_by('fullname')

    def get_serializer_class(self):

        if self.action == "list":
            return UnregisteredStudentSerializer

    def list(self, request, *args, **kwargs):

        if request.GET.get('limit', '') != '':

            student_query = self.get_queryset()

            page = self.paginate_queryset(student_query)

            serializer = self.get_serializer(page, many=True)


            return self.get_paginated_response(
                {'studentsAmount': len(student_query), 'students': serializer.data})

        serializer = self.get_serializer(self.get_queryset(), many=True)

        serializer_data = serializer.data

        return Response({'studentsAmount': len(serializer_data), 'students': serializer_data}, status.HTTP_200_OK)

class CheckAccessApiView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CheckAccessSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class UsersListView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [UsersViewPermission]
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
            if len(UploadedDocuments.objects.filter(point=point)) != len(RequiredDocuments.objects.filter(point=point)):
                continue

            self.bypassSheets |= BypassSheet.objects.filter(id=point.bypass_sheet.id)

    def __getUserBypassSheetQuery(self):

        userQuery = Student.objects.filter(user=None)

        for bypassSheet in self.bypassSheets:
            userQuery |= Student.objects.filter(user=bypassSheet.student_id.user)

        return userQuery.order_by('user__fullname')

    def __getUserPointQuery(self):
        userQuery = Student.objects.filter(user=None)

        self.__getBypassSheetQuery()

        for bypassSheet in self.bypassSheets:
            userQuery |= Student.objects.filter(user=bypassSheet.student_id.user)
        print(time.time() - self.start_time)
        return userQuery.order_by('user__fullname')

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

                students |= Student.objects.filter(group=group).select_related('user')

            new_student_query = Student.objects.filter(user=None)

            if search != "":
                for student in students:
                    if search.upper() in student.user.fullname.upper():
                        new_student_query |= Student.objects.filter(user=student.user)

                return new_student_query.order_by('user__fullname')

            return students.order_by('user__fullname')

        elif institute_title == "" and course != "" and group_title == "":

            students = Student.objects.filter(user=None)

            all_groups = Group.objects.all()
            required_groups = Group.objects.filter(id=None)

            for group in all_groups:

                course_number = group.course

                if course_number == int(course):
                    required_groups |= Group.objects.filter(id=group.id)

            for group in required_groups:
                students |= Student.objects.filter(group=group).select_related('user')

            new_student_query = Student.objects.filter(user=None)

            if search != "":
                for student in students:
                    if search.upper() in student.user.fullname.upper():
                        new_student_query |= Student.objects.filter(user=student.user)

                return new_student_query.order_by('user__fullname')

            return students.order_by('user__fullname')

        elif institute_title == "" and course == "" and group_title != "":

            students = Student.objects.filter(user=None)

            groups = Group.objects.filter(name=group_title)

            for group in groups:
                students |= Student.objects.filter(group=group).select_related('user')

            new_student_query = Student.objects.filter(user=None)

            if search != "":
                for student in students:
                    if search.upper() in student.user.fullname.upper():
                        new_student_query |= Student.objects.filter(user=student.user)

                return new_student_query.order_by('user__fullname')

            return students.order_by('user__fullname')

        elif institute_title != "" and course != "" and group_title == "":

            students = Student.objects.filter(user=None)

            institute = Institute.objects.get(title=institute_title)

            all_groups = Group.objects.filter(institute=institute)

            required_groups = Group.objects.filter(id=None)

            for group in all_groups:

                course_number = group.course

                if course_number == int(course):
                    required_groups |= Group.objects.filter(id=group.id)

            for group in required_groups:
                students |= Student.objects.filter(group=group).select_related('user')

            new_student_query = Student.objects.filter(user=None)

            if search != "":
                for student in students:
                    if search.upper() in student.user.fullname.upper():
                        new_student_query |= Student.objects.filter(user=student.user)

                return new_student_query.order_by('user__fullname')

            return students.order_by('user__fullname')

        elif((institute_title != "" and course == "" and group_title != "")
             or (institute_title != "" and course != "" and group_title != "")):

            institute = Institute.objects.get(title=institute_title)

            group = Group.objects.get(institute=institute, name=group_title)

            students = Student.objects.filter(group=group).select_related('user')

            new_student_query = Student.objects.filter(user=None)

            if search != "":
                for student in students:
                    if search.upper() in student.user.fullname.upper():
                        new_student_query |= Student.objects.filter(user=student.user)

                return new_student_query.order_by('user__fullname')

            return students.order_by('user__fullname')

        elif institute_title == "" and course != "" and group_title != "":

            students = Student.objects.filter(user=None)

            all_groups = Group.objects.filter(name=group_title)

            required_groups = Group.objects.filter(id=None)

            for group in all_groups:
                course_number = group.course

                if course_number == int(course):
                    required_groups |= Group.objects.filter(id=group.id)

            for group in required_groups:
                students |= Student.objects.filter(group=group).select_related('user')

            new_student_query = Student.objects.filter(user=None)

            if search != "":
                for student in students:
                    if search.upper() in student.user.fullname.upper():
                        new_student_query |= Student.objects.filter(user=student.user)

                return new_student_query.order_by('user__fullname')

            return students.order_by('user__fullname')

        elif institute_title == "" and course == "" and group_title == "" and search != "":
            students = Student.objects.all().select_related('user')

            new_student_query = Student.objects.filter(user=None)

            if search != "":
                for student in students:
                    if search.upper() in student.user.fullname.upper():
                        new_student_query |= Student.objects.filter(user=student.user)

                return new_student_query.order_by('user__fullname')

            return students.order_by('user__fullname')

        if self.bypassSheetsName == "":
            return Student.objects.order_by('user__fullname')

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

        self.start_time = time.time()

        if request.GET.get('limit', '') != '':

            # print(time.time() - self.start_time)

            queryset = self.get_queryset()

            page = self.paginate_queryset(self.get_serializer().setup_eager_loading(queryset))

            serializer = self.get_serializer(page, context=self.get_serializer_context(), many=True)

            serializer_data = serializer.data

            return self.get_paginated_response({'studentsAmount':len(queryset), 'students':serializer_data})

        sel_query = self.get_serializer().setup_eager_loading(self.get_queryset())

        serializer = self.get_serializer(sel_query, context=self.get_serializer_context(), many=True)

        serializer_data = serializer.data

        # print(time.time() - self.start_time)

        data_len = len(serializer_data)

        return Response({'studentsAmount':data_len, 'students':serializer_data}, status.HTTP_200_OK)

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
        if education_form == '':
            return BypassSheetTemplate.objects.all()
        return BypassSheetTemplate.objects.filter(educationForm=education_form)

    def get(self, request):

        education_form = request.GET.get('educationForm', '')

        serializer = BypassSheetTemplateTitleSerializer(self.get_queryset(education_form), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
class UploadStudents(APIView):

    permission_classes = [UploadStudentsPermission]
    #permission_classes = [AllowAny]
    def addInstitute(self, title):

        return Institute.objects.create(title=title)

    def addGroup(self, title, institute, course):

        return Group.objects.create(name=title, institute=institute, course=course)

    def addStudent(self, data):

        User.objects.filter(status="Студент").delete()

        for dictionary in data:
            institute = Institute.objects.filter(title=dictionary['Institute']).first()

            print(institute)

            if institute is None:
                institute = self.addInstitute(dictionary['Institute'])

            group = Group.objects.filter(name=dictionary['Group'], institute=institute).first()

            if group is None:
                group = self.addGroup(dictionary['Group'], institute, dictionary['Cours'])

            user = User.objects.create(fullname=dictionary['Fullname'], password=111, is_active=False,
                                       status='Студент',
                                       gender=dictionary['Gender'])

            student = Student.objects.create(user=user, group=group,
                                             educationForm=dictionary['Form of education'],
                                             recruitmentForm=dictionary['Competition'], status=dictionary['Status'],
                                             degree_of_study=dictionary['Lvl'],
                                             year_of_admission=dictionary['Year of admission'])

    def post(self, request):
        book = openpyxl.open("/back_end/Kemsu_Document_Flow/Kemsu_Document/data.xlsx",
                             read_only=True)  # change path or replace file in root dict
        sheet = book.active
        list_with_info = []
        dictionary = {}

        for row in range (2,sheet.max_row+1):
            dictionary.update(
                {"Fullname": sheet[row][0].value, "Gender": sheet[row][1].value, "Group": sheet[row][2].value,
                 "Institute": sheet[row][3].value, "Cours": sheet[row][4].value,
                 "Year of admission": sheet[row][5].value, "Specialty code": sheet[row][6].value,
                 "Specialty": sheet[row][7].value, "Lvl": sheet[row][8].value,
                 "Form of education": sheet[row][9].value, "Training period": sheet[row][10].value,
                 "Competition": sheet[row][11].value, "Academic year": sheet[row][12].value,
                 "Status": sheet[row][13].value})

            list_with_info.append(dictionary)
            print(str(row) + '/' + str(sheet.max_row))
            dictionary = {}

        self.addStudent(list_with_info)

        return Response({
            "message" : "Upload is success"
        }, status=status.HTTP_201_CREATED)

class BypassSheetSchemaDeadline(APIView):

    permission_classes = [GetBypassSheetsSchemaDeadline]
    # permission_classes = [AllowAny]

    def get(self, request):
        bypass_sheet_schemas = BypassSheetTemplate.objects.all()

        serializer = GetBypassSheetsSchemaDeadlinesSerializer(bypass_sheet_schemas, many=True, read_only=True, context={'user' : request.user})

        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateBypassSheetSchemaDeadline(GenericAPIView):
    # permission_classes = [AllowAny]
    permission_classes = [UpdateBypassSheetSchemaDeadline]
    serializer_class = PatchBypassSheetsSchemaDeadlinesSerializer

    def patch(self, request, pk):

        serializer = self.serializer_class(data=request.data, context={'id':pk})

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        data = serializer.validated_data

        return Response(status=status.HTTP_200_OK)

class DeleteExcessPointView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        students = Student.objects.all().prefetch_related('group__institute')

        for student in students:
            bypass_sheets = BypassSheet.objects.filter(student_id=student)

            points = Point.objects.filter(id=None)

            for bypass_sheet in bypass_sheets:
                points |= Point.objects.filter(bypass_sheet=bypass_sheet)

            points = points.prefetch_related('department__institute')

            for point in points:

                institute = point.department.institute

                if institute != student.group.institute and institute is not None:
                    point.delete()

        return Response(status=status.HTTP_200_OK)