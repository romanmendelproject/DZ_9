import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from courses.models import Teacher


class TeacherType(DjangoObjectType):
    class Meta:
        model = Teacher


class Query:
    all_teacher = graphene.List(TeacherType, limit=graphene.Int())

    def resolve_all_teacher(self, info, **kwargs):
        return Teacher.objects.all()
