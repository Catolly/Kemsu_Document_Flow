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
    BypassSheetsView, TokenEmailPairView,
    StudentList, LogoutView, RefreshTokenView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/signup/student', RegistrationStudentAPIView.as_view(), name='user_registration'),
    path('api/signup/staff', RegistrationStaffAPIView.as_view(), name='staff_registration'),
    path('api/login/', TokenEmailPairView.as_view(), name='token_email_pair'),
    path('api/logout/', LogoutView.as_view(), name='auth_logout'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('api/users/<int:pk>/', StudentList.as_view(), name='user_list'),
    path('api/bypass_sheets/', BypassSheetsView.as_view(), name="bypass_sheets"),
]
