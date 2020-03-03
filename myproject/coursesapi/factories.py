import factory
from django.contrib.auth.models import User

from courses.models import Course, Lesson, Student, Teacher

from .models import Place


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
    first_name = 'test'
    last_name = 'test'
    username = "test"
    email = "test@mail.com"


class TeacherFactory(factory.DjangoModelFactory):
    class Meta:
        model = Teacher
    user = factory.SubFactory(UserFactory)


class StudentFactory(factory.DjangoModelFactory):
    class Meta:
        model = Student
    user = factory.SubFactory(UserFactory)


class CourseFactory(factory.DjangoModelFactory):
    class Meta:
        model = Course
    teacher = factory.SubFactory(TeacherFactory)

class LessonFactory(factory.DjangoModelFactory):
    class Meta:
        model = Lesson
    course = factory.SubFactory(CourseFactory)

class PlaceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Place
