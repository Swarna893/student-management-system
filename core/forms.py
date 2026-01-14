from django import forms
from .models import Student, Teacher, Course, Marks

class MarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = ['marks_obtained', 'total_marks']
        widgets = {
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

# Student Form
class StudentForm(forms.ModelForm):
    """
    Form to create or update a Student.
    Includes validation to ensure unique email and roll number.
    """
    class Meta:
        model = Student
        fields = ['full_name', 'roll_number', 'email', 'course', 'dob', 'profile_photo']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}), # HTML5 Date Picker
        }

# Teacher Form
class TeacherForm(forms.ModelForm):
    """
    Form to create or update a Teacher.
    """
    class Meta:
        model = Teacher
        fields = ['name', 'email', 'assigned_courses']
        widgets = {
             'assigned_courses': forms.CheckboxSelectMultiple(), # Allow multiple course selection
        }

# Course Form
class CourseForm(forms.ModelForm):
    """
    Form to create or update a Course.
    """
    class Meta:
        model = Course
        fields = ['name', 'code', 'description']
