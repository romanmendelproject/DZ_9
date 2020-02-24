from django.contrib import admin
from courses.models import Teacher
from courses.models import Student
from courses.models import Course, Lesson


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    def first_name(self, obj):
        return obj.user.first_name
    def last_name(self, obj):
        return obj.user.last_name
    list_display = 'id', 'first_name', 'last_name', 'full_name'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    def first_name(self, obj):
        return obj.user.first_name
    def last_name(self, obj):
        return obj.user.last_name
    list_display = 'id', 'first_name', 'last_name', 'full_name'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'teacher', 'students_of_course'

    def students_of_course(self, obj):
        return "\n".join([p.full_name for p in obj.students.all()])


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'description', 'date', 'course'
