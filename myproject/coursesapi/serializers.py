from rest_framework import serializers

from courses.models import Course, Lesson, Student, Teacher


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = 'id', 'sex', 'user', 'date_of_birth', 'city', 'bio'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = 'id', 'sex', 'user', 'date_of_birth', 'city'


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = 'id', 'title', 'teacher', 'students', 'is_active'


class LessonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lesson
        fields = 'id', 'title', 'description', 'date', 'course'
