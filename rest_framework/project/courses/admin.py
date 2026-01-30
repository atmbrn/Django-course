from django.contrib import admin
from .models import Instructor, Student, Course


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'experience_years')
    search_fields = ('name', 'email')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'registered_at')
    search_fields = ('name', 'email')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'start_date')
    list_filter = ('start_date', 'instructor')
    search_fields = ('title', 'description')
