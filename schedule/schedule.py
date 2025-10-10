import grpc
import json
import requests
from concurrent import futures
from flask import request as f_request

import schedule_pb2
import schedule_pb2_grpc


USER_API = "http://localhost:3203"


def is_user_an_administrator() -> bool:
    userid = f_request.headers.get('Authorization')
    if userid is None:
        return False
    result = requests.get(USER_API+f"/users/{userid}/admin")
    if result.status_code != 200:
        return False
    return result.json()["admin"]


class ScheduleServicer(schedule_pb2_grpc.ScheduleServicer):

    def __init__(self):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]
    
    def get_all_schedule(self, request, context):
        schedule = []
        for time in self.db:
            schedule.append(schedule_pb2.ScheduleData(date=time["date"], movies_id=time["movies"]))
        return schedule_pb2.AllSchedule(all_schedule=schedule)
    
    def get_schedule_bydate(self, request, context):
        for time in self.db:
            if time["date"] == request.date:
                return schedule_pb2.ScheduleData(date=time["date"], movies_id=time["movies"])
        return schedule_pb2.ScheduleData(date="", movies_id=[])
    
    def get_dates_bymovieid(self, request, context):
        dates_list = []
        for time in self.db:
            if request.movie_id in time["movies"]:
                dates_list.append(schedule_pb2.Date(date=time["date"]))
        return schedule_pb2.DatesList(dates_list=dates_list)
    
    def schedule_movie(self, request, context):
        if not is_user_an_administrator():
            return schedule_pb2.ScheduleData(date="", movies_id=[])
        for time in self.db:
            if time["date"] == request.date:
                if not request.movie_id in time["movies"]:
                #le film n'est pas deja programme
                    time["movies"].append(request.movie_id)
                return schedule_pb2.ScheduleData(date=time["date"], movies_id=time["movies"])
        #sinon, la date n'a pas ete trouve, il faut la rajouter
        self.db.append({"date": request.date, "movies": [request.movie_id] })
        return schedule_pb2.ScheduleData(date=request.date, movies_id=[request.movie_id])
    
    def unschedule_movie(self, request, context):
        if not is_user_an_administrator():
            return schedule_pb2.ScheduledMovie(date="", movie_id="")
        for time in self.db:
            if time["date"] == request.date:
                if request.movie_id in time["movies"]:
                    time["movies"].remove(request.movie_id)
                    return schedule_pb2.ScheduledMovie(date=time["date"], movie_id=request.movie_id)
        #Si le film n'etait pas programme a cette date
        return schedule_pb2.ScheduledMovie(date="", movie_id="")
    
    def delete_movie_from_schedule(self, request, context):
        if not is_user_an_administrator():
            return schedule_pb2.DatesList(dates_list=[])
        dates_list = []
        for time in self.db:
            if request.movie_id in time["movies"]:
                time["movies"].remove(request.movie_id)
                dates_list.append(schedule_pb2.Date(date=time["date"]))
        return schedule_pb2.DatesList(dates_list=dates_list)
    
    def delete_date_from_schedule(self, request, context):
        if not is_user_an_administrator():
            return schedule_pb2.MoviesList(movies_list=[])
        movies_list = []
        for time in self.db:
            if time["date"] == request.date:
                movies_list = time["movies"]
                self.db.remove(time)
        return schedule_pb2.MoviesList(movies_list=movies_list)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    schedule_pb2_grpc.add_ScheduleServicer_to_server(ScheduleServicer(), server)
    server.add_insecure_port('[::]:3002')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
