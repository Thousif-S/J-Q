import graphene
import graphql_jwt
import works.schema
import users.schema
import works.schema_relay
import people.schema


class Query(
    users.schema.Query,
    works.schema.Query,
    works.schema_relay.RelayQuery,
    people.schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(
    users.schema.Mutation,
    works.schema.Mutation,
    works.schema_relay.RelayMutation,
    people.schema.Mutation,
    graphene.ObjectType,
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
