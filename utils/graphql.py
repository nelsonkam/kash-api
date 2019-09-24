import requests
import config


def graphql(query, variables=None):
    headers = {"x-hasura-admin-secret": config.GQL_ENGINE_SECRET}
    json = {"query": query, "variables": variables}

    resp = requests.post(config.GQL_ENGINE_URL, json=json, headers=headers)
    return resp.json()
