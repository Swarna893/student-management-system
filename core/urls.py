from django.urls import path
from . import views

urlpatterns = [
    # Dashboard (Home)
    path('', views.dashboard_view, name='dashboard'),

    # Student Section
    path('students/', views.student_list, name='students'), # URL: /students/

    # Teacher Section
    path('teachers/', views.teacher_list, name='teachers'), # URL: /teachers/

    # Course Section
    path('courses/', views.course_list, name='courses'),    # URL: /courses/

    # Add Sections (Admin Only)
    path('students/add/', views.add_student, name='add_student'),
    path('teachers/add/', views.add_teacher, name='add_teacher'),
    path('courses/add/', views.add_course, name='add_course'),

    # Detail Sections
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('teachers/<int:pk>/', views.teacher_detail, name='teacher_detail'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),

    # Edit Sections (Admin Only)
    path('students/<int:pk>/edit/', views.edit_student, name='edit_student'),
    path('teachers/<int:pk>/edit/', views.edit_teacher, name='edit_teacher'),
    path('courses/<int:pk>/edit/', views.edit_course, name='edit_course'),

    # Delete Sections (Admin Only)
    path('students/<int:pk>/delete/', views.delete_student, name='delete_student'),
    path('teachers/<int:pk>/delete/', views.delete_teacher, name='delete_teacher'),
    path('courses/<int:pk>/delete/', views.delete_course, name='delete_course'),

    # Categorized Views (Course Groups)
    path('students/by-course/', views.student_course_groups, name='student_course_groups'),
    path('students/by-course/<int:pk>/', views.students_in_group, name='students_in_group'),
    path('teachers/by-course/', views.teacher_course_groups, name='teacher_course_groups'),
    path('teachers/by-course/<int:pk>/', views.teachers_in_group, name='teachers_in_group'),

    # Marks / Results Section
    path('marks/dashboard/', views.marks_dashboard, name='marks_dashboard'),
    path('marks/course/<int:course_id>/', views.course_marks_list, name='course_marks_list'),
    path('marks/add/<int:course_id>/<int:student_id>/', views.add_marks, name='add_marks'),
    path('my-marks/', views.student_marks, name='student_marks'),
    path('student-result/<int:pk>/', views.student_result_card, name='student_result_card'), # New Result Card View
]
