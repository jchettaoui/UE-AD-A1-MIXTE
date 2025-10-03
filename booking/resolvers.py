import json
import requests

MOVIE_API = "http://localhost:3200"
SCHEDULE_API = "http://localhost:3202"

##############
#    UTIL    #
##############

def get_bookings():
    with open('{}/data/bookings.json'.format("."), "r") as file:
        bookings = json.load(file)["bookings"]
    return bookings


def save_bookings(bookings):
    with open('{}/data/bookings.json'.format("."), "w") as file:
        json.dump({"bookings":bookings}, file, indent=2)

##############
#    READ    #
##############

def user_booking_by_id(_userid: str):
    bookings = get_bookings()    
    for b in bookings:
        if b["userid"] == _userid:
            return b

def booking_record_by_user_and_date(_userid: str, _date: str):
    user_record = user_booking_by_id(_userid)
    if user_record is None:
        return
    for booking_record in user_record["dates"]:
        if booking_record["date"] == _date:
            return booking_record


def has_user_booked_a_screening(_userid: str, _date: str, _movieid: str):
    booking_record = booking_record_by_user_and_date(_userid, _date)
    if booking_record is None:
        return False
    return _movieid in booking_record["movies"]


# print(user_booking_by_id("chris_rivers"))
# print(booking_record_by_user_and_date("chris_rivers", "20151201"))
# print(has_user_booked_a_screening("chris_rivers", "20151201", "267eedb8-0f5d-42d5-8f43-72426b9fb3e6"))
# print(has_user_booked_a_screening("chris_rivers", "20151201", "bozanonzad"))


##############
#   CREATE   #
##############

def add_booking(_userid: str, _date: str, _movieid: str):
    # TODO : change API calls to use GraphQL & gRPC

    # check if movie exists
    movie_exists = requests.get(MOVIE_API+f"/movies/{_movieid}")
    if movie_exists.status_code != 200:
        return 

    # check if schedule exist
    screening_exists = requests.get(SCHEDULE_API+f"/schedule/{_date}/{_movieid}")
    if screening_exists.status_code != 200:
        return  
    
    # add booking to user
    bookings = get_bookings()
    booking_record = None
    for b in bookings:
        if b["userid"] == _userid:
            for d in b["dates"]:
                if d["date"] == _date:
                    d["movies"].append(_movieid)
                    booking_record = d
                    break
            else:
                booking_record = {"date":_date, "movies":[_movieid]}
                b["dates"].append(booking_record)
            break
    else:
        booking_record = {"date":_date, "movies":[_movieid]}
        bookings.append({"userid":_userid, "dates":[booking_record]})

    save_bookings(bookings)
    return booking_record

##############
#   DELETE   #
##############

def delete_booking(_userid: str, _date: str, _movieid: str):
    bookings = get_bookings()
    record = None

    # Most beautiful nested code ever
    for b in bookings:
        if b["userid"] == _userid:
            for d in b["dates"]:
                if d["date"] == _date:
                    if _movieid in d["movies"]:
                        d["movies"].remove(_movieid)
                        record = d
                    break
            break

    if record is None:
        return
    
    save_bookings(bookings)
    return record
