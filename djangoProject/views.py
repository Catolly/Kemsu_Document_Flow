from django.contrib.auth import login
from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.urls import reverse
'''from django.contrib.auth.models import User'''
from Kemsu_Document.models import create_employee, create_student
from Kemsu_Document.models import authenticate

class LoginView(TemplateView):
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            #user = authenticate(request, username=username, password=password)
            user = authenticate(username, password)
            if user is not None:
                login(request, user)
                return redirect(reverse("profile"))
            else:
                context['error'] = "Логин или пароль неправильные"
        return render(request, self.template_name, context)

class ProfilePage(TemplateView):
    template_name = "registration/profile.html"

class RegisterEmployee(TemplateView):
    template_name = "registration/register_employee.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            middle_name = request.POST.get('middle_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            department_name = request.POST.get('department_name')

            if password == password2:
                create_employee(first_name, last_name, middle_name, email, password, department_name)
                return redirect(reverse("login"))

        return render(request, self.template_name)

class RegisterStudent(TemplateView):
    template_name = "registration/register_student.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            middle_name = request.POST.get('middle_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            course = request.POST.get('course')
            direction_of_study = request.POST.get('direction_of_study')
            institute = request.POST.get('institute')
            group = request.POST.get('group')

            if password == password2:
                create_student(first_name, last_name, middle_name, email, password, int(course), direction_of_study, institute, group)
                return redirect(reverse("login"))

        return render(request, self.template_name)