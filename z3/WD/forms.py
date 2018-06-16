from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
import datetime

from .models import Lecturer, Course, Student, Grade


class CourseNameField(forms.CharField):
    def validate(self, value):
        super().validate(value)
        for course in Course.objects.all():
            if course.name == value or value == 'new':
                raise ValidationError(
                    _('Name: %(value)s is already in use.'), code='invalid', params={'value': value},
                )


class CourseForm(forms.Form):
    SEMESTER_CHOICES = [(a+1,a+1) for a in range(10)]
    semester = forms.ChoiceField(choices=SEMESTER_CHOICES, label='Semester' )
    LECTURER_CHOICES = Lecturer.objects.all()
    lecturer = forms.ModelChoiceField(queryset=LECTURER_CHOICES, label='Lecturer')
    course_name = CourseNameField(label='Course name', max_length=256)


class CourseStudentsForm(forms.Form):

    students_lists = forms.ModelMultipleChoiceField(Student.objects.all())

    def __init__(self, students, *args, **kwargs):
        super(CourseStudentsForm, self).__init__(*args, **kwargs)
        self.fields['students_lists'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=students, label='Students')


class GradeForm(forms.Form):
    GRADE_CHOICES = [((a)/2+2,(a)/2+2) for a in range(7)]
    grade = forms.ChoiceField(label='Grade', choices=GRADE_CHOICES)
    GRADE_TABLE_CHOICES = Grade.objects.filter(grade__isnull=True)
    date = forms.DateField(initial=datetime.date.today)
    grade_table = forms.ModelChoiceField(queryset=GRADE_TABLE_CHOICES, label='Select student and course: ')

