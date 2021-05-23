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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import re_path, include
from . import settings

from .views import (
    RegistrationStudentAPIView, RegistrationStaffAPIView,
    BypassSheetsView, UserList,
    LogoutView, RefreshTokenView,
    LoginView, BypassSheetView, DepartmentsView, CheckAccessApiView,
    GroupApiView, BypassSheetsTemplateApiView, BypassSheetTemplateApiView, UnregisteredStudentListApiView,
    UsersListView, BanApiView, UnbanApiView, BypassSheetTemplateTitle
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/signup/student/', RegistrationStudentAPIView.as_view(), name='user_registration'),
    path('api/signup/staff/', RegistrationStaffAPIView.as_view(), name='staff_registration'),
    path('api/logout/', LogoutView.as_view(), name='auth_logout'),
    path('api/token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('api/users/<int:pk>/', UserList.as_view(), name='student_list'),
    path('api/users/', UsersListView.as_view({'get': 'list'}), name='students_list_view'),
    path('api/bypass_sheets/', BypassSheetsView.as_view(), name="bypass_sheets"),
    path('api/bypass_sheets/<int:pk>/', BypassSheetView.as_view(), name="bypass_sheet"),
    path('api/login/', LoginView.as_view(), name="login"),
    path('api/departments/', DepartmentsView.as_view(), name="departments_view"),
    path('api/groups/', GroupApiView.as_view(), name='group'),
    path('api/bypass_sheets_schema/', BypassSheetsTemplateApiView.as_view(), name='bypass-sheets-template'),
    path('api/bypass_sheets_schema/<int:pk>/', BypassSheetTemplateApiView.as_view(), name='bypass-sheet-template'),
    path('api/unregistered_students/', UnregisteredStudentListApiView.as_view({'get': 'list'}), name='unregistered-students'),
    path('api/checkAccess', CheckAccessApiView.as_view(), name='check-access'),
    path('api/ban/<int:pk>/', BanApiView.as_view(), name='ban'),
    path('api/unban/<int:pk>', UnbanApiView.as_view(), name='unban'),
    path('api/bypass_sheets_schema/titles', BypassSheetTemplateTitle.as_view(), name='bypass-sheet-template-title')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)