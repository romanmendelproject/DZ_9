import graphene

from coursesapi.schema import Query as LectureQuery

from coursesapi.schema import Mutation as LectureMutation


class Query(LectureQuery, graphene.ObjectType):
    pass


class Mutation(LectureMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
