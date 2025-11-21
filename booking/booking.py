import argparse

from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType, MutationType
from flask import Flask, request, jsonify, make_response

from model import BookingResolvers
from model.db import BookingDatabaseConnector, BookingDatabaseConnectorJson, BookingDatabaseConnectorMongo

########################################################################################
#                                                                                      #
#                                    CONFIGURATION                                     #
#                                                                                      #
########################################################################################

# Storage
DEFAULT_JSON_DESTINATION = "./data/bookings.json"
DEFAULT_MONGO_DESTINATION = "mongodb://root:example@localhost:27017/"

# Web app
PORT = 3003
HOST = '0.0.0.0'

# External services
DEFAULT_MOVIE_API_URL = "http://localhost:3200"
DEFAULT_SCHEDULE_API_URL = "http://localhost:3202"
DEFAULT_USER_API_URL = "http://localhost:3203"

movie_api_url = None
schedule_api_url = None
user_api_url = None

########################################################################################
#                                                                                      #
#                                  VARIABLES GLOBALES                                  #
#                                                                                      #
########################################################################################

app = Flask(__name__)
database : BookingDatabaseConnector = None
r : BookingResolvers = None
schema = None

########################################################################################
#                                                                                      #
#                                FONCTIONS UTILITAIRES                                 #
#                                                                                      #
########################################################################################

def parse_args() -> None:
   """Parse command line arguments to choose data storage method and destination."""

   parser = argparse.ArgumentParser()
   parser.add_argument("-m", "--mongo", help="Choose mongodb as data storage", action="store_true")
   parser.add_argument("-j", "--json", help="Choose JSON file as data storage", action="store_true")
   parser.add_argument("--storage", help="Specify where the data is stored (either a json file or a mongo url)")
   parser.add_argument("--user-service-url", help="Specify the url of the user service", default=DEFAULT_USER_API_URL)
   parser.add_argument("--movie-service-url", help="Specify the url of the movie service", default=DEFAULT_MOVIE_API_URL)
   parser.add_argument("--schedule-service-url", help="Specify the url of the schedule service", default=DEFAULT_SCHEDULE_API_URL)

   args = parser.parse_args()

   if not args.mongo and not args.json:
      print("Please select a data storage method when starting the app : \n\tJSON : -j \n\tMongoDB : -m\nYou can also specify the storage destination with the flag '--storage'")
      exit(1)

   if args.mongo and args.json:
      print("You can only choose one data storage method !")
      exit(1)

   destination = ""
   if not args.storage:
      print("No storage destination found. Using default value :", end="")
      if args.mongo:
         print(DEFAULT_MONGO_DESTINATION)
         destination = DEFAULT_MONGO_DESTINATION
      else:
         # Json by default
         print(DEFAULT_JSON_DESTINATION)
         destination = DEFAULT_JSON_DESTINATION
   else:
      destination = args.storage

   global database, user_api_url, movie_api_url, schedule_api_url

   if args.mongo:
      database = BookingDatabaseConnectorMongo(destination)
   else:
      # Json by default
      database = BookingDatabaseConnectorJson(destination)

   user_api_url = args.user_service_url
   movie_api_url = args.movie_service_url
   schedule_api_url = args.schedule_service_url


def init_graphql() -> None:
    global schema, r

    r = BookingResolvers(database, movie_api_url, schedule_api_url, user_api_url)

    type_defs = load_schema_from_path('booking.graphql')

    query = QueryType()
    query.set_field('user_booking_by_id', r.user_booking_by_id)
    query.set_field('booking_record_by_user_and_date', r.booking_record_by_user_and_date)
    query.set_field('has_user_booked_a_screening', r.has_user_booked_a_screening)

    mutation = MutationType()
    mutation.set_field('add_booking', r.add_booking)
    mutation.set_field('delete_booking', r.delete_booking)

    user_record = ObjectType('UserRecord')
    booking_record = ObjectType('BookingRecord')

    schema = make_executable_schema(type_defs, user_record, booking_record, query, mutation)

########################################################################################
#                                                                                      #
#                                        ROUTES                                        #
#                                                                                      #
########################################################################################

# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>",200)

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