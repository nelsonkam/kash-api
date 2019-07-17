from graphqlclient import GraphQLClient
import config

client = GraphQLClient(config.GQL_ENGINE_URL)

client.inject_token(config.GQL_ENGINE_SECRET)