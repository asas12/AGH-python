from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


from .models import Student, Course, Lecturer, Grade
from .forms import CourseForm, CourseStudentsForm, GradeForm


def index(request):
    return render(request, 'WD/index.html')


def course_info(request, course_name):
    course = Course.objects.get(name=course_name)
    students_list = Student.objects.filter(course=course)
    course = get_object_or_404(Course, name=course_name)
    return render(request, 'WD/course_info.html', {'course': course, 'students_list':students_list})


def courses_overview(request):
    courses_list = Course.objects.order_by('semester', 'name')[::]
    context = {
        'courses_list': courses_list,
    }
    return render(request, 'WD/courses_overview.html', context)


def choose_students_for_course(request, semester, lecturer_id, course_name):
    if request.method == 'POST':
        students = Student.objects.filter(semester=semester)
        form = CourseStudentsForm(students, request.POST)
        if form.is_valid():
            lecturer=Lecturer.objects.get(id=lecturer_id)
            course = Course.objects.create(lecturer=lecturer, name=course_name, semester=semester)
            for student in form.cleaned_data['students_lists']:
                g = Grade(student=student, course=course)
                g.save()
            return HttpResponseRedirect(reverse('WD:course_created'))
    else:
        students = Student.objects.filter(semester=semester)
        form = CourseStudentsForm(students=students)
    return render(request, 'WD/choose_students.html', {'form': form, 'semester':semester, 'lecturer':Lecturer.objects.get(id=lecturer_id), 'course_name':course_name})


def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            semester = form.cleaned_data['semester']
            lecturer = form.cleaned_data['lecturer']
            course_name = form.cleaned_data['course_name']
            return HttpResponseRedirect(reverse('WD:choose_students', args=(semester,lecturer.id,course_name)))
    else:
        form = CourseForm()
    return render(request, 'WD/create_course.html', {'form': form})

'''old_version
def create_course(request):
    lecturer_list = Lecturer.objects.order_by('lastname', 'firstname')[::]
    if request.method == "POST":
        try:
            s = request.POST['semester']
        except(KeyError):
            return render(request, 'WD/create_course.html',
                          {'range': range(10),'lecturer_list': lecturer_list, 'error_message': "You didn't select any semester."})
        try:
            l = request.POST['lecturer']
        except(KeyError):
            return render(request, 'WD/create_course.html',
                          {'range': range(10), 'lecturer_list': lecturer_list, 'error_message': "You didn't select any lecturer. s = {}".format(s)})
        try:
            course_name = request.POST['course_name']
        except(KeyError):
            return render(request, 'WD/create_course.html',
                          {'range': range(10), 'lecturer_list': lecturer_list, 'error_message': "You didn't put course name in."})

        response = 'You have chosen {} semester'
        return render(request, 'WD/create_course.html',
                      {'range': range(10), 'lecturer_list': lecturer_list,
                       'error_message': "OK. s={}, l={}, cn={}".format(s,l,course_name)})

    else:
        return render(request, 'WD/create_course.html', {'range': range(10), 'lecturer_list': lecturer_list})
'''


def course_created(request):
    return render(request, 'WD/course_created.html')


def student_info(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'WD/student_info.html', {'student': student})


def students_overview(request):
    students_list = Student.objects.order_by('semester', 'lastname', 'firstname')[::]
    context = {
        'students_list': students_list,
    }
    return render(request, 'WD/students_overview.html', context)


def student_grade(request, student_id, course_name):
    student = Student.objects.get(id=student_id)
    course = Course.objects.get(name=course_name)
    grade = Grade.objects.get(student=student, course=course)
    response = "You're looking at student's {} grade for course {}. Given {}. Grade: {}"
    return HttpResponse(response.format(student, course, grade.date, grade.grade))


def student_grades(request, student_id):
    student = Student.objects.get(id=student_id)
    grades_list = Grade.objects.filter(student=student)
    context = {
        'grades_list' : grades_list,
        'student': student,
    }
    return render(request, 'WD/student_grades.html', context)


def give_grade(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.cleaned_data['grade']
            date = form.cleaned_data['date']
            grade_table = form.cleaned_data['grade_table']
            grade_table.grade = grade
            grade_table.date = date
            grade_table.save()
            student = Student.objects.get(grade=grade_table)
            course = Course.objects.get(grade=grade_table)
            return HttpResponseRedirect(reverse('WD:student_grade', args=(student.id, course.name)))
    else:
        form = GradeForm()
    return render(request, 'WD/give_grade.html', {'form': form})
