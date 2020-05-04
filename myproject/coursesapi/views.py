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
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


# class UserViewSet(viewsets.ModelViewSet, BaseAuthentication):
#     def get_queryset(self):
#         user = User.objects.all()
#         print (self.request.user)
#         return user
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
    

# class UserViewSet(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     def get(self, request):
#         print(request.user)
#         serializer = UserSerializer(request.user)
#         return Response(serializer.data)
# class UserViewSet(APIView):
#     def get(self, request, format=None):
#         usernames = [user.username for user in User.objects.all()]
#         return Response(usernames)
