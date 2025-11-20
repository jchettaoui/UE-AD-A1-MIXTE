import argparse
from flask import Flask, request as f_request, jsonify, make_response
from model import UserDatabaseConnector, UserDatabaseJsonConnector, UserDatabaseMongoConnector

########################################################################################
#                                                                                      #
#                                    CONFIGURATION                                     #
#                                                                                      #
########################################################################################

# Storage
DEFAULT_JSON_DESTINATION = "./data/users.json"
DEFAULT_MONGO_DESTINATION = "mongodb://root:example@localhost:27017/"

# Web app
PORT = 3203
HOST = '0.0.0.0'

########################################################################################
#                                                                                      #
#                                  VARIABLES GLOBALES                                  #
#                                                                                      #
########################################################################################

app = Flask(__name__)
database : UserDatabaseConnector = None

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
      destination = parser.storage

   global database

   if args.mongo:
      database = UserDatabaseMongoConnector(destination)
   else:
      # Json by default
      database = UserDatabaseJsonConnector(destination)


def authorization_is_admin() -> bool:
   auth_value = f_request.headers.get('Authorization')
   if auth_value is None:
      return False
   user = database.get_user_by_id(auth_value)
   if user is None:
      return False
   return user["admin"]


def authorization_is_admin_or_self(userid: str) -> bool:
   auth_value = f_request.headers.get('Authorization')
   if auth_value is None:
      return False
   if userid == auth_value:
      return True
   user = database.get_user_by_id(auth_value)
   if user is None:
      return False
   return user["admin"]

########################################################################################
#                                                                                      #
#                                        ROUTES                                        #
#                                                                                      #
########################################################################################

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/users", methods=["GET"])
def route_get_all_users():
   if not authorization_is_admin():
      return make_response(jsonify({"error":"Unauthorized route"}), 403)
   users = database.get_users()
   return make_response(jsonify(users),200)


@app.route("/users/<user_id>", methods=["GET"])
def route_get_user_by_id(user_id: str):
   user = database.get_user_by_id(user_id)
   if user is None:
      return make_response(jsonify({"error":"User not found"}), 404)
   database.update_user(user["id"], user)
   return make_response(jsonify(user),200)


@app.route("/users/<user_id>", methods=["DELETE"])
def route_delete_user(user_id: str):
   if not authorization_is_admin_or_self(user_id):
      return make_response(jsonify({"error":"Unauthorized route"}), 403)
   user = database.get_user_by_id(user_id)
   if user is None:
      return make_response(jsonify({"error":"User not found"}), 404)
   database.delete_user(user["id"])
   return make_response(jsonify({"message":"User deleted", "user":user}), 200)


@app.route("/users/<user_id>/<user_name>", methods=["POST"])
def route_add_user(user_id: str, user_name: str):
   user = database.get_user_by_id(user_id)
   if user is not None:
      return make_response(jsonify({"error":"User already exists"}), 400)
   user = {
      "id": user_id,
      "name": user_name,
      "admin": False
   }
   database.create_user(user)
   return make_response(jsonify({"message":"User created", "user":user}), 201)


@app.route("/users/<user_id>/<new_name>", methods=["PUT"])
def route_edit_user_name(user_id: str, new_name: str):
   if not authorization_is_admin_or_self(user_id):
      return make_response(jsonify({"error":"Unauthorized route"}), 403)
   user = database.get_user_by_id(user_id)
   if user is None:
      return make_response(jsonify({"error":"User not found"}), 404)
   user["name"] = new_name
   database.update_user(user["id"], user)
   return make_response(jsonify(user),200)


@app.route("/users/<user_id>/admin", methods=["GET"])
def route_is_user_admin(user_id: str):
   """Check if a user is an administrator"""
   user = database.get_user_by_id(user_id)
   if user is None:
      return make_response(jsonify({"error":"User not found"}), 404)
   return make_response(jsonify({"userid":user_id, "admin":user["admin"]}))


@app.route("/users/<user_id>/admin/yes", methods=["PUT"])
def route_edit_user_promote_admin(user_id: str):
   """Grant admin privileges to a user"""
   if not authorization_is_admin():
      return make_response(jsonify({"error":"Unauthorized route"}), 403)
   user = database.get_user_by_id(user_id)
   if user is None:
      return make_response(jsonify({"error":"User not found"}), 404)
   user["admin"] = True
   database.update_user(user["id"], user)
   return make_response(jsonify({"message":"User is now admin", "user_id":user_id}), 200)


@app.route("/users/<user_id>/admin/no", methods=["PUT"])
def route_edit_user_demote_admin(user_id: str):
   """Remove admin privileges from a user"""
   if not authorization_is_admin():
      return make_response(jsonify({"error":"Unauthorized route"}), 403)
   user = database.get_user_by_id(user_id)
   if user is None:
      return make_response(jsonify({"error":"User not found"}), 404)
   user["admin"] = False
   database.update_user(user["id"], user)
   return make_response(jsonify({"message":"User is no longer admin", "user_id":user_id}), 200)

########################################################################################
#                                                                                      #
#                                      DEMARRAGE                                       #
#                                                                                      #
########################################################################################

if __name__ == "__main__":
   parse_args()
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
