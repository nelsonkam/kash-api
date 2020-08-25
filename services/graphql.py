from ariadne import load_schema_from_path, make_executable_schema, graphql_sync, fallback_resolvers
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify, Blueprint, current_app as app

from resolvers import query
from resolvers.extensions import QueryExecutionExtension

type_defs = load_schema_from_path("schemas")
schema = make_executable_schema(type_defs, query)
blueprint = Blueprint("graphql", __name__, url_prefix="/graphql")


@blueprint.route("", methods=["GET"])
def graphql_playground():
    # On GET request serve GraphQL Playground
    # You don't need to provide Playground if you don't want to
    # but keep on mind this will not prohibit clients from
    # exploring your API using desktop GraphQL Playground app.
    return PLAYGROUND_HTML, 200


@blueprint.route("", methods=["POST"])
def graphql_server():
    # GraphQL queries are always sent as POST
    data = request.get_json()

    # Note: Passing the request to the context is optional.
    # In Flask, the current request is always accessible as flask.request
    success, result = graphql_sync(schema, data, context_value=request, debug=app.debug, extensions=[QueryExecutionExtension])

    status_code = 200 if success else 400
    return jsonify(result), status_code
