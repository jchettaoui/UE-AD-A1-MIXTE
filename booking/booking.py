from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType, MutationType
from flask import Flask, request, jsonify, make_response

import resolvers as r

PORT = 3003
HOST = '0.0.0.0'
app = Flask(__name__)

# todo create elements for Ariadne
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

if __name__ == "__main__":
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)