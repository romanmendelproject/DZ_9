from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from courses.models import Course, Lesson, Student, Teacher

from .serializers import (CourseSerializer, LessonSerializer,
                          StudentSerializer, TeacherSerializer, UserSerializer)

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from requests.api import request


class TeacherViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class StudentViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
