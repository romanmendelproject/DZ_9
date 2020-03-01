from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APISimpleTestCase, APITransactionTestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth.models import User
from .models import Place
from courses.models import Teacher, Student, Course, Lesson
from .factories import TeacherFactory, CourseFactory, StudentFactory, LessonFactory, UserFactory, PlaceFactory
from .views import TeacherViewSet, StudentViewSet, CourseViewSet, LessonViewSet


# Testing via api SimpleTest
class TestCaseForTeacherSimple(APISimpleTestCase):
    def test_create_city_request_factory(self):
        teacher = TeacherFactory.build(city="Moscow", sex=1, bio='abc',)
        self.assertEqual(teacher.city, "Moscow")

class TestCaseForStudentSimple(APISimpleTestCase):
    def test_create_student_request_factory(self):
        student = StudentFactory.build(city="Moscow", sex=1,)
        self.assertEqual(student.city, "Moscow")

class TestCaseForCourseSimple(APISimpleTestCase):
    def test_create_course_request_factory(self):
        course = CourseFactory.build(title="Test",)
        self.assertEqual(course.title, "Test")

class TestCaseForLessonSimple(APISimpleTestCase):
    def test_create_lesson_request_factory(self):
        lesson = LessonFactory.build(title="Test",)
        self.assertEqual(lesson.title, "Test")

# Testing JWT Auth
class TestAuthJWT(APITestCase):
    def test_api_jwt(self):
        u = User.objects.create_user(username='testuser', email='testuser@foo.com', password='testuser')
        u.is_active = True
        u.save()
        resp = self.client.post('/coursesapi/token/', {'username':'testuser', 'password':'testuser'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in resp.data)


class TestCaseForTeacher(APITestCase):
    @classmethod
    def setUpTestData(cls):
        u = User.objects.create_user(username='testuser', email='testuser@foo.com', password='testuser')
        u.is_active = True
        u.save()

    # Testing via api client
    def test_get_teacher_api_client(self):
        teacher = TeacherFactory(city="Moscow", sex=1, bio='abc',)
        resp = self.client.post('/coursesapi/token/', {'username':'testuser', 'password':'testuser'}, format='json')
        token = resp.data['access']  
        response = self.client.get("/coursesapi/api/teacher/",  format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get("/coursesapi/api/teacher/",  format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_teacher_api_client(self):
        resp = self.client.post('/coursesapi/token/', {'username':'testuser', 'password':'testuser'}, format='json')
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token) 
        response = self.client.post(
            "/coursesapi/api/teacher/", data={"sex": 1, "user": 1, "date_of_birth": "2000-01-01", "city": "town", "bio": "test"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestCaseForStudent(APITestCase):

    # Testing via request factory
    def test_get_student_request_factory(self):
        student = StudentFactory(city="Moscow", sex=1,)
        request_factory = APIRequestFactory()
        request = request_factory.get("/coursesapi/api/student/")
        student_view = StudentViewSet.as_view({"get": "list"})
        response = student_view(request).render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_student_request_factory(self):
        request_factory = APIRequestFactory()
        user = UserFactory()
        request = request_factory.post(
            "/coursesapi/api/student/", {"sex": 1, "user": 1, "date_of_birth": "2000-01-01", "city": "town"}, format="json")
        student_view = StudentViewSet.as_view({"post": "create"})
        response = student_view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Testing via api client
    def test_get_city_api_client(self):
        student = StudentFactory(city="Moscow", sex=1,)
        response = self.client.get("/coursesapi/api/student/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_student_api_client(self):
        user = UserFactory()
        response = self.client.post(
            "/coursesapi/api/student/", data={"sex": 1, "user": 1, "date_of_birth": "2000-01-01", "city": "town"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class TestCaseForCourse(APITestCase):

    # Testing via request factory
    def test_get_course_request_factory(self):
        course = CourseFactory(title="Test",)
        request_factory = APIRequestFactory()
        request = request_factory.get("/coursesapi/api/course/")
        course_view = CourseViewSet.as_view({"get": "list"})
        response = course_view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_course_request_factory(self):
        request_factory = APIRequestFactory()
        student = StudentFactory(city="Moscow", sex=1,)
        request = request_factory.post(
            "/coursesapi/api/course/", {"title": "test", "students" : ["/coursesapi/api/student/1/"]}, format="json")
        course_view = CourseViewSet.as_view({"post": "create"})
        response = course_view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Testing via api client
    def test_get_course_api_client(self):
        course = CourseFactory(title="Test",)
        response = self.client.get("/coursesapi/api/course/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_course_api_client(self):
        student = StudentFactory(city="Moscow", sex=1,)
        response = self.client.post(
            "/coursesapi/api/course/", data={"title": "test", "students" : ["/coursesapi/api/student/1/"]}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class TestCaseForLesson(APITestCase):

    # Testing via request factory
    def test_get_lesson_request_factory(self):
        lesson = LessonFactory(title="Test",)
        request_factory = APIRequestFactory()
        request = request_factory.get("/coursesapi/api/lesson/")
        lesson_view = LessonViewSet.as_view({"get": "list"})
        response = lesson_view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_lesson_request_factory(self):
        request_factory = APIRequestFactory()
        course = CourseFactory(title="Test",)
        request = request_factory.post(
            "/coursesapi/api/lesson/", {"title": "test", "course" : "/coursesapi/api/course/1/"}, format="json")
        lesson_view = LessonViewSet.as_view({"post": "create"})
        response = lesson_view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Testing via api client
    def test_get_lesson_api_client(self):
        lesson = LessonFactory(title="Test",)
        response = self.client.get("/coursesapi/api/lesson/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_lesson_api_client(self):
        course = CourseFactory(title="Test",)
        response = self.client.post(
            "/coursesapi/api/lesson/", data={"title": "test", "course" : "/coursesapi/api/course/1/"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestCaseForPlace(APITestCase):
    def test_transactional_case_for_city(self):
        PlaceFactory(name="TestName", street="TestStreet", street_number=10, office=20)
        place = Place.objects.first()
        place.set_office()
        self.assertNotEqual(place.change, True)


class TestCaseForCityWithTransaction(APITransactionTestCase):
    def test_transactional_case_for_city(self):
        PlaceFactory(name="TestName", street="TestStreet", street_number=10, office=20)
        place = Place.objects.first()
        place.set_office()
        self.assertEqual(place.change, True)