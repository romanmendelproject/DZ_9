from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import (APIRequestFactory, APISimpleTestCase,
                                 APITestCase, APITransactionTestCase)

from courses.models import Course, Lesson, Student, Teacher

from .factories import (CourseFactory, LessonFactory, PlaceFactory,
                        StudentFactory, TeacherFactory, UserFactory)
from .models import Place
from .views import CourseViewSet, LessonViewSet, StudentViewSet, TeacherViewSet


class TestCaseForTeacherSimple(APISimpleTestCase):
    """
    Testing via api SimpleTest Teacher
    """
    def test_create_city_request_factory(self):
        teacher = TeacherFactory.build(city="Moscow", sex=Teacher.SEX_WOMAN, bio='abc')
        self.assertEqual(teacher.city, "Moscow")
        self.assertEqual(teacher.sex, Teacher.SEX_WOMAN)
        self.assertEqual(teacher.bio, "abc")


class TestCaseForStudentSimple(APISimpleTestCase):
    """
    Testing via api SimpleTest Student
    """
    def test_create_student_request_factory(self):
        student = StudentFactory.build(city="Moscow", sex=Student.SEX_WOMAN)
        self.assertEqual(student.city, "Moscow")
        self.assertEqual(student.sex, Teacher.SEX_WOMAN)


class TestCaseForCourseSimple(APISimpleTestCase):
    """
    Testing via api SimpleTest Course
    """
    def test_create_course_request_factory(self):
        course = CourseFactory.build(title="Test")
        self.assertEqual(course.title, "Test")


class TestCaseForLessonSimple(APISimpleTestCase):
    """
    Testing via api SimpleTest Lesson
    """
    def test_create_lesson_request_factory(self):
        lesson = LessonFactory.build(title="Test")
        self.assertEqual(lesson.title, "Test")


class TestAuthJWT(APITestCase):
    """
    Testing JWT Auth
    """
    def test_api_jwt(self):
        u = User.objects.create_user(username='testuser', email='testuser@foo.com', password='testuser')
        u.is_active = True
        u.save()
        resp = self.client.post('/coursesapi/token/', {'username': 'testuser', 'password': 'testuser'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in resp.data)


class TestCaseForTeacher(APITestCase):
    """
    Testing Teacher via api client and request factory
    """
    @classmethod
    def setUpTestData(cls):
        cls.request_factory = APIRequestFactory()
        u = User.objects.create_user(username='testuser', email='testuser@foo.com', password='testuser')
        u.is_active = True
        u.save()

    def setUp(self):
        resp = self.client.post('/coursesapi/token/', {'username': 'testuser', 'password': 'testuser'}, format='json')
        self.token = resp.data['access']

    # Testing via api client
    def test_get_teacher_api_client(self):
        teacher = TeacherFactory(city="Moscow", sex=Teacher.SEX_WOMAN, bio='abc',)
        response = self.client.get("/coursesapi/api/teacher/",  format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get("/coursesapi/api/teacher/",  format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_teacher_api_client(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(
            "/coursesapi/api/teacher/", data={"sex": Teacher.SEX_WOMAN, "user": 1, "date_of_birth": "2000-01-01", "city": "town", "bio": "test"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_teacher_request_factory(self):
        teacher = TeacherFactory(city="Moscow", sex=Teacher.SEX_WOMAN,)
        request = self.request_factory.get("/coursesapi/api/teacher/", HTTP_AUTHORIZATION='Bearer ' + self.token)
        teacher_view = TeacherViewSet.as_view({"get": "list"})
        response = teacher_view(request).render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_teacher_request_factory(self):
        request = self.request_factory.post(
            "/coursesapi/api/teacher/", {"sex": Teacher.SEX_WOMAN, "user": 1, "date_of_birth": "2000-01-01", "city": "town", "bio": "test"}, HTTP_AUTHORIZATION='Bearer ' + self.token)
        teacher_view = TeacherViewSet.as_view({"post": "create"})
        response = teacher_view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestCaseForStudent(APITestCase):
    """
    Testing Student via api client and request factory
    """
    @classmethod
    def setUpTestData(cls):
        cls.request_factory = APIRequestFactory()

    # Testing via request factory
    def test_get_student_request_factory(self):
        student = StudentFactory(city="Moscow", sex=Teacher.SEX_WOMAN,)
        request = self.request_factory.get("/coursesapi/api/student/")
        student_view = StudentViewSet.as_view({"get": "list"})
        response = student_view(request).render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_student_request_factory(self):
        user = UserFactory()
        request = self.request_factory.post(
            "/coursesapi/api/student/", {"sex": Teacher.SEX_WOMAN, "user": 1, "date_of_birth": "2000-01-01", "city": "town"}, format="json")
        student_view = StudentViewSet.as_view({"post": "create"})
        response = student_view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Testing via api client
    def test_get_city_api_client(self):
        student = StudentFactory(city="Moscow", sex=Teacher.SEX_WOMAN,)
        response = self.client.get("/coursesapi/api/student/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_student_api_client(self):
        user = UserFactory()
        response = self.client.post(
            "/coursesapi/api/student/", data={"sex": Teacher.SEX_WOMAN, "user": 1, "date_of_birth": "2000-01-01", "city": "town"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestCaseForCourse(APITestCase):
    """
    Testing Course via api client and request factory
    """
    @classmethod
    def setUpTestData(cls):
        cls.request_factory = APIRequestFactory()

    # Testing via request factory
    def test_get_course_request_factory(self):
        course = CourseFactory(title="Test",)
        request = self.request_factory.get("/coursesapi/api/course/")
        course_view = CourseViewSet.as_view({"get": "list"})
        response = course_view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_course_request_factory(self):
        student = StudentFactory(city="Moscow", sex=1,)
        request = self.request_factory.post(
            "/coursesapi/api/course/", {"title": "test", "students": ["/coursesapi/api/student/1/"]}, format="json")
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
    """
    Testing Lesson via api client and request factory
    """
    @classmethod
    def setUpTestData(cls):
        cls.request_factory = APIRequestFactory()

    @classmethod
    def setUpClass(cls):
        super(TestCaseForLesson, cls).setUpClass()
        Course.objects.create(title="Test")
        Lesson.objects.create(title="Test", course_id=1)

    #Testing via request factory
    def test_get_lesson_request_factory(self):
        request = self.request_factory.get("/coursesapi/api/lesson/")
        lesson_view = LessonViewSet.as_view({"get": "list"})
        response = lesson_view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_lesson_request_factory(self):
        request = self.request_factory.post(
            "/coursesapi/api/lesson/", {"title": "test", "course": "/coursesapi/api/course/1/"}, format="json")
        lesson_view = LessonViewSet.as_view({"post": "create"})
        response = lesson_view(request)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Testing via api client
    def test_get_lesson_api_client(self):
        response = self.client.get("/coursesapi/api/lesson/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_lesson_api_client(self):
        response = self.client.post(
            "/coursesapi/api/lesson/", data={"title": "test", "course": "/coursesapi/api/course/1/"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestCaseForPlace(APITestCase):
    """
    Testing Place without APITransactionTestCase
    """
    def test_transactional_case_for_city(self):
        PlaceFactory(name="TestName", street="TestStreet", street_number=10, office=20)
        place = Place.objects.first()
        place.set_office()
        self.assertNotEqual(place.change, True)


class TestCaseForCityWithTransaction(APITransactionTestCase):
    """
    Testing Place via APITransactionTestCase
    """
    def test_transactional_case_for_city(self):
        PlaceFactory(name="TestName", street="TestStreet", street_number=10, office=20)
        place = Place.objects.first()
        place.set_office()
        self.assertEqual(place.change, True)
