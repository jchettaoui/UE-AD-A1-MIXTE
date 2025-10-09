from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType, MutationType
from flask import Flask, request, jsonify, make_response

import resolvers as r

PORT = 3001
HOST = '0.0.0.0'
app = Flask(__name__)

# todo create elements for Ariadne
type_defs = load_schema_from_path('movie.graphql')
query = QueryType()
movie = ObjectType('Movie')
query.set_field('movie_with_id', r.movie_with_id)
mutation = MutationType()
mutation.set_field('update_movie_rate', r.update_movie_rate)
actor = ObjectType('Actor')
movie.set_field('actors', r.resolve_actors_in_movie)
query.set_field('actor_with_id', r.actor_with_id)
query.set_field('movie_by_title', r.movie_by_title)
mutation.set_field('add_movie_to_actor', r.add_movie_to_actor)
mutation.set_field('add_movie', r.add_movie)
mutation.set_field('delete_movie_by_id', r.delete_movie_by_id)
mutation.set_field('delete_movie_by_title', r.delete_movie_by_title)
mutation.set_field('add_new_actor', r.add_new_actor)
schema = make_executable_schema(type_defs, movie, query, mutation, actor)

# graphql entry points
@app.route('/graphql', methods=['POST'])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
                        schema,
                        data,
                        context_value=None,
                        debug=app.debug
                    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

if __name__ == "__main__":
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)