import graphene
from products.schema import Query as ProductsQuery, Mutation as ProductsMutation

class Query(ProductsQuery, graphene.ObjectType):
    pass

class Mutation(ProductsMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)