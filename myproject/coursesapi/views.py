from courses.models import Teacher, Student, Course, Lesson
from .serializers import TeacherSerializer, StudentSerializer, CourseSerializer, LessonSerializer
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated


class TeacherViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer