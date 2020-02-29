import graphene
from courses.models import Teacher
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField





# from .models import School, City
#
#
class TeacherType(DjangoObjectType):
    class Meta:
        model = Teacher

#
# class TeacherFilteredType(DjangoObjectType):
#
#     class Meta:
#         model = Teacher
#         filter_fields = {
#             'name': ['exact', 'icontains', 'istartswith'],
#         }
#         interfaces = (graphene.relay.Node, )
#
#
# # class CityType(DjangoObjectType):
# #
# #     class Meta:
# #         model = City
#
#
# class TeacherMutation(graphene.Mutation):
#
#     class Arguments:
#         school_id = graphene.Int(required=True)
#         new_name = graphene.String(required=True)
#
#     result = graphene.Boolean()
#     teacher = graphene.Field(SchoolType)
#
#     def mutate(self, info, school_id, new_name):
#         # TODO
#         return {
#             'result': True,
#             'school': Teacher.objects.first()
#         }
#
#
# class Mutation:
#     change_teacher_name = TeacherMutation.Field()
#
#
class Query:
    all_teacher = graphene.List(TeacherType, limit=graphene.Int())
#     filtered_teachers = DjangoFilterConnectionField(TeacherFilteredType)
#     retrieve_teacher = graphene.Field(TeacherType, id=graphene.Int())
#
#     def resolve_all_schools(self, *args, **kwargs):
#         if 'limit' in kwargs:
#             return Teacher.objects.all()[:kwargs['limit']]
#         return Teacher.objects.all()
#
    def resolve_all_teacher(self, info, **kwargs):
        return Teacher.objects.all()