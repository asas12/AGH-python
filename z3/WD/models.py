from django.db import models
import datetime


class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=40)
    email = models.EmailField(blank=True)
    semester = models.IntegerField(default=1)

    def __str__(self):
        return self.firstname+' '+self.lastname


class Lecturer(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=40)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.firstname+' '+self.lastname


class Course(models.Model):
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, through='Grade')
    name = models.CharField(max_length=200)
    semester = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.FloatField(blank=True, null=True)
    date = models.DateField(blank=True, null=True, default=datetime.date.today)

    def __str__(self):
        return self.student.__str__() + ' ' + self.course.__str__()
