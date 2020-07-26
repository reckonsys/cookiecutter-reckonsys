from graphene import ObjectType, Schema

from backend.core.mutations import CoreMutation
from backend.core.queries import CoreQuery


class Query(
        CoreQuery,

        # lastly,
        ObjectType):
    pass


class Mutation(
        CoreMutation,

        # lastly,
        ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutation)
