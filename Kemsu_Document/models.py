from django.db import models


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.IntegerField()
    direction_of_study = models.CharField(max_length=75)
    institute = models.CharField(max_length=75)
    group = models.CharField(max_length=30)


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=75)


class Administrator(models.Model):
    id = models.AutoField(primary_key=True)


class Document(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=75)
    #point = models.CharField(max_length=75)
    # data = models.CharField(max_length=75)
    link_on_Student = models.ForeignKey(Student, on_delete=models.CASCADE)


class Point(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=75)
    description = models.TextField()
    file = models.FileField()
    link_on_module = models.ForeignKey(Document, on_delete=models.CASCADE)

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    First_name = models.CharField(max_length=75)
    Last_name = models.CharField(max_length=75)
    Midle_name = models.CharField(max_length=75)
    role_in_the_system = models.CharField(max_length=30)
    e_mail = models.EmailField()
    link_on_Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    link_on_Employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    link_on_Administrator = models.ForeignKey(Administrator, on_delete=models.CASCADE)
