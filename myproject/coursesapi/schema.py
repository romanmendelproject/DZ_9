import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from courses.models import Teacher, Student, Course, Lesson


class TeacherType(DjangoObjectType):
    class Meta:
        model = Teacher


class StudentType(DjangoObjectType):
    class Meta:
        model = Student


class CourseType(DjangoObjectType):
    class Meta:
        model = Course


class LessonType(DjangoObjectType):
    class Meta:
        model = Lesson


class UserType(DjangoObjectType):
    class Meta:
        model = User


class CourseFilteredType(DjangoObjectType):
    """
    Filter Course query
    """
    class Meta:
        model = Course
        filter_fields = {
            'title': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (graphene.relay.Node, )


class CourseMutation(graphene.Mutation):
    """
    Mutation Course query
    """
    class Arguments:
        course_id = graphene.Int(required=True)
        new_title = graphene.String(required=True)

    result = graphene.Boolean()
    course = graphene.Field(CourseType)

    def mutate(self, info, course_id, new_title):
        Course.objects.filter(id=course_id).update(title=new_title)
        return {
            'result': True,
            'course': Course.objects.get(id=course_id)
        }


class Mutation:
    change_course_name = CourseMutation.Field()


class Query:
    all_teacher = graphene.List(TeacherType)
    all_course = graphene.List(CourseType, limit=graphene.Int())
    all_lesson = graphene.List(LessonType, limit=graphene.Int())
    retrieve_course = graphene.Field(CourseType, id=graphene.Int())
    filtered_course = DjangoFilterConnectionField(CourseFilteredType)

    def resolve_all_teacher(self, info, **kwargs):
        """
        All teachers query
        """
        return Teacher.objects.all()

    def resolve_all_course(self, info, **kwargs):
        """
        All courses query with limit
        """
        if 'limit' in kwargs:
            return Course.objects.all()[:kwargs['limit']]
        return Course.objects.all()

    def resolve_all_lesson(self, info, **kwargs):
        """
        All lessons query with limit
        """
        if 'limit' in kwargs:
            return Lesson.objects.all()[:kwargs['limit']]
        return Lesson.objects.all()

    def resolve_retrieve_course(self, info, **kwargs):
        """
        Course query with filter
        """
        if 'id' in kwargs:
            return Course.objects.get(id=kwargs["id"])
