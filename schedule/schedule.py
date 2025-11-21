import grpc
import argparse
import requests
from concurrent import futures
from flask import request as f_request

from model.api import MovieApiWrapper, UserApiWrapper
from model.db import ScheduleDatabaseMongoConnector, ScheduleDatabaseConnector, ScheduleDatabaseJsonConnector

import schedule_pb2
import schedule_pb2_grpc

########################################################################################
#                                                                                      #
#                                    CONFIGURATION                                     #
#                                                                                      #
########################################################################################

# Storage
DEFAULT_JSON_DESTINATION = "./data/times.json"
DEFAULT_MONGO_DESTINATION = "mongodb://root:example@localhost:27017/"

# External services
DEFAULT_MOVIE_API_URL = "http://localhost:3001"
DEFAULT_USER_API_URL = "http://localhost:3203"

########################################################################################
#                                                                                      #
#                                  VARIABLES GLOBALES                                  #
#                                                                                      #
########################################################################################

database : ScheduleDatabaseConnector = None
movie_api : MovieApiWrapper = None
user_api : UserApiWrapper = None

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

    global database, user_api

    if args.mongo:
        database = ScheduleDatabaseMongoConnector(destination)
    else:
        # Json by default
        database = ScheduleDatabaseJsonConnector(destination)

    user_api = UserApiWrapper(args.user_service_url)
    movie_api = MovieApiWrapper(args.movie_service_url)


def is_user_an_administrator(context) -> bool:
    metadata = dict(context.invocation_metadata())
    userid = metadata.get("authorization")
    if userid is None:
        return False
    return user_api.is_user_an_administrator(userid)


########################################################################################
#                                                                                      #
#                                        ROUTES                                        #
#                                                                                      #
########################################################################################

class ScheduleServicer(schedule_pb2_grpc.ScheduleServicer):

    def __init__(self, database):
        self.db = database

    def route_get_all_schedule(self, request, context):
        donnees = self.db.get_schedule()

        schedule = []
        for time in donnees:
            schedule.append(schedule_pb2.ScheduleData(date=time["date"], movies_id=time["movies"]))
        return schedule_pb2.AllSchedule(all_schedule=schedule)
    
    def route_get_schedule_bydate(self, request, context):
        time = self.db.get_schedule_by_date(request.date)
        if time is not None: 
            return schedule_pb2.ScheduleData(date=time["date"], movies_id=time["movies"])  
        return schedule_pb2.ScheduleData(date="", movies_id=[])
    
    def route_get_dates_bymovieid(self, request, context):
        schedule_list = self.db.get_schedule_by_movieid(request.movie_id)
        dates_list = []
        for time in schedule_list:
            dates_list.append(schedule_pb2.Date(date=time["date"]))
        return schedule_pb2.DatesList(dates_list=dates_list)
    
    def route_schedule_movie(self, request, context):
        if not is_user_an_administrator(context):
            return schedule_pb2.ScheduleData(date="", movies_id=[])
        
        date_movie = self.db.add_movie_to_date(request.date, request.movie_id)
        if date_movie is not None:
            return schedule_pb2.ScheduleData(date=date_movie["date"], movies_id=date_movie["movies"])
        
        #sinon la date n'a pas été trouvé
        self.db.add_date_to_schedule({"date": request.date, "movies": [request.movie_id] })
        return schedule_pb2.ScheduleData(date=request.date, movies_id=[request.movie_id])
    
    def route_unschedule_movie(self, request, context):
        if not is_user_an_administrator(context):
            return schedule_pb2.ScheduledMovie(date="", movie_id="")
        deleted_movie = self.db.delete_movie_from_date(request.date, request.movie_id)
        if deleted_movie is not None: 
            return schedule_pb2.ScheduledMovie(date=deleted_movie["date"], movie_id=request.movie_id)
        #Si le film n'etait pas programme a cette date
        return schedule_pb2.ScheduledMovie(date="", movie_id="")
    
    def route_delete_movie_from_schedule(self, request, context):
        if not is_user_an_administrator(context):
            return schedule_pb2.DatesList(dates_list=[])
        
        schedule_list = self.db.delete_movie_from_schedule(request.movie_id)
        dates_list = []
        for time in schedule_list:
            dates_list.append(schedule_pb2.Date(date=time["date"]))

        return schedule_pb2.DatesList(dates_list=dates_list)
    
    def route_delete_date_from_schedule(self, request, context):
        if not is_user_an_administrator(context):
            return schedule_pb2.MoviesList(movies_list=[])
        movies_list = self.db.delete_date_from_schedule(request.date)
        return schedule_pb2.MoviesList(movies_list=movies_list)

########################################################################################
#                                                                                      #
#                                      DEMARRAGE                                       #
#                                                                                      #
########################################################################################

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    schedule_pb2_grpc.add_ScheduleServicer_to_server(ScheduleServicer(database), server)
    server.add_insecure_port('[::]:3002')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    parse_args()
    serve()
