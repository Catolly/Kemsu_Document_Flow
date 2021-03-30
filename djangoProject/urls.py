"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from django.urls import re_path, include

from .views import (
    RegistrationStudentAPIView, RegistrationStaffAPIView,
    GroupList, InstituteList, ModuleList,
    PointList, BypassSheetsView, PostByPassSheetsView,
    GetByPassSheetsDetailView, TokenEmailPairView, TokenUsernamePairView, StudentList, LogoutView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
'''from djangoProject.views import RegisterEmployee, LoginView, ProfilePage, RegisterStudent
from djangoProject.views import HomeView, ContactsView, LoginView'''

'''path('accounts/login/', LoginView.as_view(), name="login"),
    path('accounts/profile/', ProfilePage.as_view(), name="profile"),
    path('admin/', admin.site.urls),
    path('accounts/register/employee', RegisterEmployee.as_view(), name="register_employee"),
    path('accounts/register/student', RegisterStudent.as_view(), name="register_student")'''

urlpatterns = [
    path('api/signup/student', RegistrationStudentAPIView.as_view(), name='user_registration'),
    path('api/signup/staff', RegistrationStaffAPIView.as_view(), name='staff_registration'),
    #path('login/', LoginAPIView.as_view(), name='user_login'),
    #path('api-auth', include('rest_framework.urls')),
    #path('api/login/fio/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/login/fio/', TokenUsernamePairView.as_view(), name='token_username_pair'),
    path('api/login/', TokenEmailPairView.as_view(), name='token_email_pair'),
    path('api/logout/', LogoutView.as_view(), name='auth_logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/admin/', admin.site.urls),
    # path('api/department/', DepartmentList.as_view(), name='department_list'),
    # path('api/group/', GroupList.as_view(), name='group_list'),
    # path('api/institute/', InstituteList.as_view(), name='institute_list'),
    # path('api/module/', ModuleList.as_view(), name='module_list'),
    # path('api/point/', PointList.as_view(), name='point_list'),
    # path('api/staff/', StaffList.as_view(), name='staff_list'),
    # path('api/student/', StudentList.as_view(), name='student_list'),
    path('api/users/<int:pk>/', StudentList.as_view(), name='user_list'),
    path('api/bypass_sheets/', BypassSheetsView.as_view(), name="bypass_sheets"),
    # path('api/<int:pk>/bypasssheets/create/', PostByPassSheetsView.as_view(), name="post_bypass_sheets"),
    # path('api/bypassshets/<int:pk>/detail', GetByPassSheetsDetailView.as_view(), name="get_bypass_sheets_detail")
]
