import graphene


class Query(graphene.ObjectType):
    test = graphene.Boolean()

    def resolve_test(root, info):
        return True


schema = graphene.Schema(query=Query)
