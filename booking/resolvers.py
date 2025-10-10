import json
import requests
import grpc
from flask import request as f_request

import schedule_pb2
import schedule_pb2_grpc


MOVIE_API = "http://localhost:3001"
SCHEDULE_API = "localhost:3002"
USER_API = "http://localhost:3203"

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


def get_schedule_by_date(_date):
    with grpc.insecure_channel(SCHEDULE_API) as channel:
        stub = schedule_pb2_grpc.ScheduleStub(channel)
        schedule = schedule_pb2.Date(date=_date)
        result, call = stub.get_schedule_bydate.with_call(schedule)
    channel.close()
    return result, call.code()


def is_user_an_administrator(userid) -> bool:
    if userid is None:
        return False
    result = requests.get(USER_API+f"/users/{userid}/admin")
    if result.status_code != 200:
        return False
    return result.json()["admin"]

##############
#    READ    #
##############

def user_booking_by_id(_,info, _userid: str):
    auth_value = f_request.headers.get('Authorization')
    if auth_value != _userid and not is_user_an_administrator(auth_value):
        return
    
    bookings = get_bookings()    
    for b in bookings:
        if b["userid"] == _userid:
            return b

def booking_record_by_user_and_date(_,info,_userid: str, _date: str):
    auth_value = f_request.headers.get('Authorization')
    if auth_value != _userid and not is_user_an_administrator(auth_value):
        return
    
    user_record = user_booking_by_id(_,info, _userid)
    if user_record is None:
        return
    for booking_record in user_record["dates"]:
        if booking_record["date"] == _date:
            return booking_record


def has_user_booked_a_screening(_,info, _userid: str, _date: str, _movieid: str):
    auth_value = f_request.headers.get('Authorization')
    if auth_value != _userid and not is_user_an_administrator(auth_value):
        return
    
    booking_record = booking_record_by_user_and_date(_,info, _userid, _date)
    if booking_record is None:
        return False
    return _movieid in booking_record["movies"]

##############
#   CREATE   #
##############

def add_booking(_,info,_userid: str, _date: str, _movieid: str):
    auth_value = f_request.headers.get('Authorization')
    if auth_value != _userid and not is_user_an_administrator(auth_value):
        return

    # check if movie exists
    movie_exists = requests.post(
        MOVIE_API+f"/graphql", 
        json={"query": "{movie_with_id(" +f"_id:\"{_movieid}\")"+"{title}}"}
    )
    if movie_exists.status_code != 200:
        return

    # check if schedule exist
    screening, request_code = get_schedule_by_date(_date)
    if request_code != grpc.StatusCode.OK or screening.date == "":
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

def delete_booking(_,info,_userid: str, _date: str, _movieid: str):
    auth_value = f_request.headers.get('Authorization')
    if auth_value != _userid and not is_user_an_administrator(auth_value):
        return
    
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
