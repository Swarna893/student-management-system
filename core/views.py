from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import views as auth_views
from django.contrib import messages
from .models import Student, Teacher, Course, Marks
from .forms import StudentForm, TeacherForm, CourseForm, MarksForm

# Role Checks
def is_admin(user):
    return user.is_superuser

def is_teacher(user):
    return hasattr(user, 'teacher')

def is_student(user):
    return hasattr(user, 'student')

# Dashboard View
@login_required
def dashboard_view(request):
    if is_admin(request.user):
        return render(request, 'dashboard/admin_dashboard.html', get_admin_context())
    elif is_teacher(request.user):
        return render(request, 'dashboard/teacher_dashboard.html', get_teacher_context(request.user))
    elif is_student(request.user):
        return render(request, 'dashboard/student_dashboard.html', get_student_context(request.user))
    else:
        # Fallback or unrelated user
        return render(request, 'dashboard.html')

# Context Helpers
def get_admin_context():
    return {
        'total_students': Student.objects.count(),
        'total_teachers': Teacher.objects.count(),
        'total_courses': Course.objects.count(),
    }

def get_teacher_context(user):
    return {
        'courses': user.teacher.assigned_courses.all()
    }

def get_student_context(user):
    marks = Marks.objects.filter(student=user.student)
    return {
        'student': user.student,
        'marks': marks
    }

# Decorators
def admin_required(view_func):
    return user_passes_test(is_admin)(view_func)

def teacher_required(view_func):
    return user_passes_test(is_teacher)(view_func)

# ---------------------------------------------------
# NEW VIEWS FOR NAVIGATION (Students, Teachers, Courses)
# ---------------------------------------------------

@login_required
def student_list(request):
    """
    View to list all students.
    Fetches all student records and renders 'students/student_list.html'.
    """
    students = Student.objects.all() # Fetch all students from database
    return render(request, 'students/student_list.html', {'students': students})

@login_required
def teacher_list(request):
    """
    View to list all teachers.
    Fetches all teacher records and renders 'teachers/teacher_list.html'.
    """
    teachers = Teacher.objects.all() # Fetch all teachers from database
    return render(request, 'teachers/teacher_list.html', {'teachers': teachers})

@login_required
def course_list(request):
    """
    View to list all courses.
    Fetches all course records and renders 'courses/course_list.html'.
    """
    courses = Course.objects.all() # Fetch all courses from database
    return render(request, 'courses/course_list.html', {'courses': courses})

# ---------------------------------------------------
# ADD VIEWS (Admin Only)
# ---------------------------------------------------

@login_required
@admin_required
def add_student(request):
    """
    View to add a new student.
    Only accessible by Admins.
    """
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES) # Handle file upload (profile_photo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully!')
            return redirect('students')
    else:
        form = StudentForm()
    
    return render(request, 'students/add_student.html', {'form': form})

@login_required
@admin_required
def add_teacher(request):
    """
    View to add a new teacher.
    Only accessible by Admins.
    """
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher added successfully!')
            return redirect('teachers')
    else:
        form = TeacherForm()
    
    return render(request, 'teachers/add_teacher.html', {'form': form})

@login_required
@admin_required
def add_course(request):
    """
    View to add a new course.
    Only accessible by Admins.
    """
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course added successfully!')
            return redirect('courses')
    else:
        form = CourseForm()
    
    return render(request, 'courses/add_course.html', {'form': form})

# ---------------------------------------------------
# DETAIL VIEWS
# ---------------------------------------------------

@login_required
def student_detail(request, pk):
    """
    View to show details of a single student.
    """
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/student_detail.html', {'student': student})

@login_required
def teacher_detail(request, pk):
    """
    View to show details of a single teacher.
    """
    teacher = get_object_or_404(Teacher, pk=pk)
    return render(request, 'teachers/teacher_detail.html', {'teacher': teacher})

@login_required
def course_detail(request, pk):
    """
    View to show details of a single course.
    """
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course})

# ---------------------------------------------------
# EDIT VIEWS (Admin Only)
# ---------------------------------------------------

@login_required
@admin_required
def edit_student(request, pk):
    """
    View to edit an existing student.
    Only accessible by Admins.
    """
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('student_detail', pk=pk)
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'students/edit_student.html', {'form': form, 'student': student})

@login_required
@admin_required
def edit_teacher(request, pk):
    """
    View to edit an existing teacher.
    Only accessible by Admins.
    """
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher updated successfully!')
            return redirect('teacher_detail', pk=pk)
    else:
        form = TeacherForm(instance=teacher)
    
    return render(request, 'teachers/edit_teacher.html', {'form': form, 'teacher': teacher})

@login_required
@admin_required
def edit_course(request, pk):
    """
    View to edit an existing course.
    Only accessible by Admins.
    """
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('course_detail', pk=pk)
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'courses/edit_course.html', {'form': form, 'course': course})
    return render(request, 'courses/edit_course.html', {'form': form, 'course': course})

# ---------------------------------------------------
# DELETE VIEWS (Admin Only)
# ---------------------------------------------------

@login_required
@admin_required
def delete_student(request, pk):
    """
    View to delete a student.
    Only accessible by Admins.
    """
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('students')
    
    return render(request, 'students/delete_student.html', {'student': student})

@login_required
@admin_required
def delete_teacher(request, pk):
    """
    View to delete a teacher.
    Only accessible by Admins.
    """
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, 'Teacher deleted successfully!')
        return redirect('teachers')
    
    return render(request, 'teachers/delete_teacher.html', {'teacher': teacher})

@login_required
@admin_required
def delete_course(request, pk):
    """
    View to delete a course.
    Only accessible by Admins.
    """
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        return redirect('courses')
    
    return render(request, 'courses/delete_course.html', {'course': course})

# ---------------------------------------------------
# CATEGORIZED VIEWS (New Request)
# ---------------------------------------------------

@login_required
def student_course_groups(request):
    """
    View to list courses for the purpose of viewing student groups.
    """
    courses = Course.objects.all()
    return render(request, 'students/course_groups.html', {'courses': courses})

@login_required
def students_in_group(request, pk):
    """
    View to list students in a specific course group.
    """
    course = get_object_or_404(Course, pk=pk)
    students = Student.objects.filter(course=course)
    return render(request, 'students/students_in_group.html', {'course': course, 'students': students})

@login_required
def teacher_course_groups(request):
    """
    View to list courses for the purpose of viewing teacher groups.
    """
    courses = Course.objects.all()
    return render(request, 'teachers/course_groups.html', {'courses': courses})

@login_required
def teachers_in_group(request, pk):
    """
    View to list teachers in a specific course group.
    """
    course = get_object_or_404(Course, pk=pk)
    # Teacher has ManyToManyField 'assigned_courses'
    teachers = Teacher.objects.filter(assigned_courses=course)
    return render(request, 'teachers/teachers_in_group.html', {'course': course, 'teachers': teachers})
    
    return render(request, 'students/delete_student.html', {'student': student})

@login_required
@admin_required
def delete_teacher(request, pk):
    """
    View to delete a teacher.
    Only accessible by Admins.
    """
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, 'Teacher deleted successfully!')
        return redirect('teachers')
    
    return render(request, 'teachers/delete_teacher.html', {'teacher': teacher})

@login_required
@admin_required
def delete_course(request, pk):
    """
    View to delete a course.
    Only accessible by Admins.
    """
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        return redirect('courses')
    
    return render(request, 'courses/delete_course.html', {'course': course})

# ---------------------------------------------------
# MARKS / RESULTS SECTION
# ---------------------------------------------------

@login_required
def marks_dashboard(request):
    """
    Dashboard for teachers to see their courses and manage marks.
    Students can also see a link to their own marks here if needed, 
    but we'll make a separate view for them.
    This view is primarily for TEACHERS to select a course.
    """
    if is_teacher(request.user):
        courses = request.user.teacher.assigned_courses.all()
        return render(request, 'marks/marks_dashboard.html', {'courses': courses})
    elif is_admin(request.user):
        courses = Course.objects.all()
        return render(request, 'marks/marks_dashboard.html', {'courses': courses})
    else:
        messages.error(request, "Access denied. Teachers only.")
        return redirect('dashboard')

@login_required
def course_marks_list(request, course_id):
    """
    List of students in a course with their marks.
    Teachers can select a student to add/edit marks.
    """
    course = get_object_or_404(Course, pk=course_id)
    
    # Permission check: Admin or the assigned teacher
    if not is_admin(request.user):
        if not hasattr(request.user, 'teacher') or course not in request.user.teacher.assigned_courses.all():
             messages.error(request, "You are not assigned to this course.")
             return redirect('marks_dashboard')

    students = Student.objects.filter(course=course)
    
    # We want to show existing marks if any
    student_marks = []
    for student in students:
        mark = Marks.objects.filter(student=student, course=course).first()
        student_marks.append({
            'student': student,
            'mark': mark
        })
    
    return render(request, 'marks/course_marks_list.html', {'course': course, 'student_marks': student_marks})

@login_required
def add_marks(request, course_id, student_id):
    """
    Form to add or edit marks for a specific student in a specific course.
    """
    course = get_object_or_404(Course, pk=course_id)
    student = get_object_or_404(Student, pk=student_id)
    
    # Permission check
    if not is_admin(request.user):
        if not hasattr(request.user, 'teacher') or course not in request.user.teacher.assigned_courses.all():
             messages.error(request, "You are not assigned to this course.")
             return redirect('marks_dashboard')
    
    # Check if mark already exists
    existing_mark = Marks.objects.filter(student=student, course=course).first()
    
    if request.method == 'POST':
        form = MarksForm(request.POST, instance=existing_mark)
        if form.is_valid():
            mark = form.save(commit=False)
            mark.student = student
            mark.course = course
            mark.save()
            messages.success(request, f'Marks saved for {student.full_name}')
            return redirect('course_marks_list', course_id=course.id)
    else:
        form = MarksForm(instance=existing_mark)
        
    return render(request, 'marks/add_marks.html', {
        'form': form, 
        'course': course, 
        'student': student
    })

@login_required
def student_marks(request):
    """
    View for a STUDENT to see their own marks across all courses.
    """
    if not is_student(request.user):
        messages.error(request, "Access denied. Students only.")
        return redirect('dashboard')
        
    student = request.user.student
    marks = Marks.objects.filter(student=student)
    
    return render(request, 'marks/student_marks.html', {'marks': marks, 'student': student})

@login_required
def student_result_card(request, pk):
    """
    View for Admins/Teachers to see a specific student's result card.
    """
    student = get_object_or_404(Student, pk=pk)
    
    # Permission check
    if not (is_admin(request.user) or is_teacher(request.user)):
         messages.error(request, "Access denied.")
         return redirect('dashboard')
         
    marks = Marks.objects.filter(student=student)
    return render(request, 'marks/student_marks.html', {'marks': marks, 'student': student})
