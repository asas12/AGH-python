from django.urls import path

from . import views

app_name= 'WD'
urlpatterns = [
    path('', views.index, name='index'),
    path('students/', views.students_overview, name='students_overview'),
    path('courses/', views.courses_overview, name='courses_overview'),
    path('courses/new/', views.create_course, name='create_course'),
    path('courses/new/course_created', views.course_created, name='course_created'),
    path('courses/new/<int:semester><int:lecturer_id><str:course_name>', views.choose_students_for_course, name='choose_students'),
    path('courses/<str:course_name>/', views.course_info, name='course_info'),
    path('students/<int:student_id>/', views.student_info, name='student_info'),
    path('grades/<int:student_id>/', views.student_grades, name='student_grades'),
    path('grades/<int:student_id>/<str:course_name>/', views.student_grade, name='student_grade'),
    path('grades/give/', views.give_grade, name='give_grade'),

]