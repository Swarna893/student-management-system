from django.contrib import admin
from .models import Course, Student, Teacher, Attendance, Marks

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'roll_number', 'course', 'email')
    list_filter = ('course',)
    search_fields = ('full_name', 'roll_number', 'email')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'status')
    list_filter = ('course', 'date', 'status')
    search_fields = ('student__full_name', 'course__name')

@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'marks_obtained', 'total_marks')
    list_filter = ('course',)
    search_fields = ('student__full_name', 'course__name')
