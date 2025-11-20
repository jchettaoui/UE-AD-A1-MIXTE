import argparse

from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType, MutationType
from flask import Flask, request, jsonify, make_response

from model import MovieResolvers
from model.db import MovieDatabaseConnector, MovieDatabaseJsonConnector, MovieDatabaseMongoConnector, ActorDatabaseConnector, ActorDatabaseJsonConnector, ActorDatabaseMongoConnector

########################################################################################
#                                                                                      #
#                                    CONFIGURATION                                     #
#                                                                                      #
########################################################################################

# Storage
DEFAULT_JSON_MOVIE_DESTINATION = "./data/movies.json"
DEFAULT_JSON_ACTOR_DESTINATION = "./data/actors.json"
DEFAULT_MONGO_DESTINATION = "mongodb://root:example@localhost:27017/"

# Web app
PORT = 3001
HOST = '0.0.0.0'

# External services 
USER_API = "http://localhost:3203"

########################################################################################
#                                                                                      #
#                                  VARIABLES GLOBALES                                  #
#                                                                                      #
########################################################################################

app = Flask(__name__)
database_movie : MovieDatabaseConnector = None
database_actor : ActorDatabaseConnector = None
r: MovieResolvers = None
schema = None

################################################################################################
#                                                                                              #
#                                  FONCTIONS UTILITAIRES                                       #
#                                                                                              #
################################################################################################

def parse_args() -> None:
   """Parse command line arguments to choose data storage method and destination."""

   parser = argparse.ArgumentParser()
   parser.add_argument("-m", "--mongo", help="Choose mongodb as data storage", action="store_true")
   parser.add_argument("-j", "--json", help="Choose JSON file as data storage", action="store_true")
   parser.add_argument("--storage_movies", help="Specify where the movies data is stored (either a json file or a mongo url)")
   parser.add_argument("--storage_actors", help="Specify where the actors data is stored (either a json file or a mongo url)")

   args = parser.parse_args()

   if not args.mongo and not args.json:
      print("Please select a data storage method when starting the app : \n\tJSON : -j \n\tMongoDB : -m\nYou can also specify the storage destination with the flag '--storage'")
      exit(1)

   if args.mongo and args.json:
      print("You can only choose one data storage method !")
      exit(1)

   destination_movies = ""
   if not args.storage_movies:
      print("No storage_movies destination found. Using default value :", end="")
      if args.mongo:
         print(DEFAULT_MONGO_DESTINATION)
         destination_movies = DEFAULT_MONGO_DESTINATION
      else:
         # Json by default
         print(DEFAULT_JSON_MOVIE_DESTINATION)
         destination_movies = DEFAULT_JSON_MOVIE_DESTINATION
   else:
      destination_movies = args.storage_movies

   destination_actors = ""
   if not args.storage_actors:
      print("No storage_actors destination found. Using default value :", end="")
      if args.mongo:
         print(DEFAULT_MONGO_DESTINATION)
         destination_actors = DEFAULT_MONGO_DESTINATION
      else:
         # Json by default
         print(DEFAULT_JSON_ACTOR_DESTINATION)
         destination_actors = DEFAULT_JSON_ACTOR_DESTINATION
   else:
      destination_actors = args.storage_actors

   global database_movie
   global database_actor

   if args.mongo:
      database_movie = MovieDatabaseMongoConnector(destination_movies)
      database_actor = ActorDatabaseMongoConnector(destination_actors)
   else:
      # Json by default
      database_movie = MovieDatabaseJsonConnector(destination_movies)
      database_actor = ActorDatabaseJsonConnector(destination_actors)


def init_graphql() -> None:
    global schema, r

    r = MovieResolvers(database_movie, database_actor, USER_API)
    type_defs = load_schema_from_path('movie.graphql')
    
    movie = ObjectType('Movie')
    actor = ObjectType('Actor')
    movie.set_field('actors', r.route_resolve_actors_in_movie)

    #query
    query = QueryType()
    query.set_field('movie_with_id', r.route_movie_by_id)
    query.set_field('actor_with_id', r.route_actor_by_id)
    query.set_field('movie_by_title', r.route_movie_by_title)

    #mutation
    mutation = MutationType()
    mutation.set_field('update_movie_rate', r.route_update_movie_rate)
    mutation.set_field('add_movie_to_actor', r.route_add_movie_to_actor)
    mutation.set_field('add_movie', r.route_add_movie)
    mutation.set_field('delete_movie_by_id', r.route_delete_movie_by_id)
    mutation.set_field('delete_movie_by_title', r.route_delete_movie_by_title)
    mutation.set_field('add_new_actor', r.route_add_new_actor)

    schema = make_executable_schema(type_defs, movie, query, mutation, actor)

#######################################################################################
#                                                                                     #
#                                        ROUTES                                       #
#                                                                                     #
#######################################################################################

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

########################################################################################
#                                                                                      #
#                                      DEMARRAGE                                       #
#                                                                                      #
########################################################################################

if __name__ == "__main__":
    parse_args()
    init_graphql()
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)