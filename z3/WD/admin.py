from django.contrib import admin
from .models import Student, Lecturer, Grade, Course

admin.site.register(Student)
admin.site.register(Lecturer)
admin.site.register(Grade)
admin.site.register(Course)

