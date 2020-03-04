import json

from graphene_django.utils.testing import GraphQLTestCase
from myproject.schema import schema
from courses.models import Course

class GQLTestCase(GraphQLTestCase):

    GRAPHQL_SCHEMA = schema

    def test_all_course_query(self):
        """
        Testing Course via all_course
        """
        response = self.query(
            '''
            query {
                allCourse{
                    title
                }
            }
            ''',
            op_name='allCourse'
            )

        self.assertResponseNoErrors(response)

    def test_all_teacher_query(self):
        """
        Testing Teacher via all_teacher
        """
        response = self.query(
            '''
            query {
                allTeacher{
                    city
                }
            }
            ''',
            op_name='allTeacher'
        )

        self.assertResponseNoErrors(response)

    def test_all_lesson_query(self):
        """
        Testing Teacher via all_lesson
        """
        response = self.query(
            '''
            query {
                allLesson{
                    title
                }
            }
            ''',
            op_name='allLesson'
        )

        self.assertResponseNoErrors(response)

    def test_retrieve_course_query(self):
        """
        Testing Course via retrieve_course
        """
        Course.objects.create(title="Test")
        response = self.query(
            '''
            query {
                retrieveCourse(id:1){
                    title
                    }
            }
            ''',
            op_name='retrieveCourse'
        )

        self.assertResponseNoErrors(response)

    def test_changeCourseName_query(self):
        """
        Testing via changeCourseName
        """
        Course.objects.create(title="Test")
        response = self.query(
            '''
            mutation{
                changeCourseName(courseId:1, newTitle:"test"){
                    result
                    course{
                        title
                    }
                }
            }
            ''',
            op_name='changeCourseName'
        )

        self.assertResponseNoErrors(response)
