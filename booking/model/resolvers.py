import json
import requests
import grpc
from flask import request as f_request

from .db import BookingDatabaseConnector
from .api import MovieApiWrapper, ScheduleApiWrapper, UserApiWrapper


class BookingResolvers:
    
    def __init__(self, db_connector: BookingDatabaseConnector, movie_api_url: str, schedule_api_url: str, user_api_url: str):
        self._database = db_connector
        self._movie_api = MovieApiWrapper(movie_api_url)
        self._schedule_api = ScheduleApiWrapper(schedule_api_url)
        self._user_api = UserApiWrapper(user_api_url)

    ##############
    #    READ    #
    ##############

    def user_booking_by_id(self, _, info, _userid: str):
        auth_value = f_request.headers.get('Authorization')
        if auth_value != _userid and not self._user_api.is_user_an_administrator(auth_value):
            return
        
        bookings = self._database.get_bookings()
        for b in bookings:
            if b["userid"] == _userid:
                return b

    def booking_record_by_user_and_date(self, _, info, _userid: str, _date: str):
        auth_value = f_request.headers.get('Authorization')
        if auth_value != _userid and not self._user_api.is_user_an_administrator(auth_value):
            return
        
        return self._database.get_booking_by_user_and_date(_userid, _date)


    def has_user_booked_a_screening(self, _, info, _userid: str, _date: str, _movieid: str):
        auth_value = f_request.headers.get('Authorization')
        if auth_value != _userid and not self._user_api.is_user_an_administrator(auth_value):
            return
        
        booking_record = self._database.get_booking_by_user_and_date(_userid, _date)
        if booking_record is None:
            return False
        return _movieid in booking_record["movies"]    

    ##############
    #   CREATE   #
    ##############

    def add_booking(self, _, info, _userid: str, _date: str, _movieid: str):
        auth_value = f_request.headers.get('Authorization')
        if auth_value != _userid and not self._user_api.is_user_an_administrator(auth_value):
            return

        # check if movie exists
        movie_exists = self._movie_api.get_movie_by_id(_movieid)
        if movie_exists.status_code != 200:
            return

        # check if schedule exist
        screening, request_code = self._schedule_api.get_schedule_by_date(_date)
        if request_code != grpc.StatusCode.OK or screening.date == "":
            return
        
        # add booking to user
        self._database.add_booking(_userid, _date, _movieid)
        return self._database.get_booking_by_user_and_date(_userid, _date)

    ##############
    #   DELETE   #
    ##############

    def delete_booking(self, _, info, _userid: str, _date: str, _movieid: str):
        auth_value = f_request.headers.get('Authorization')
        if auth_value != _userid and not self._user_api.is_user_an_administrator(auth_value):
            return        
        record = self._database.delete_booking(_userid, _date, _movieid)
        return record
