from .schedule_database_connector import ScheduleDatabaseConnector
from typing import List

from pymongo import MongoClient


class ScheduleDatabaseMongoConnector(ScheduleDatabaseConnector):

    def __init__(self, db_url: str):
        super().__init__()
        self._db_url = db_url
        self._client = MongoClient(self._db_url)
        self._db = self._client["schedule"]
        print(f"Initialized Schedule Database Mongo Connector with file_path: {db_url}")

    def get_schedule(self):
        collection = self._db["schedule"]
        schedule = list(collection.find())
        return schedule
    
    def get_schedule_by_date(self, date):
        collection = self._db["schedule"]
        schedule = collection.find_one(
            {"date": date},
            {"_id": 0, "date": 1, "movies": 1}
        )
        return schedule
    
    def get_schedule_by_movieid(self, movie_id):
        collection = self._db["schedule"]
        schedule_list = list(collection.find({"movies": movie_id}))
        return schedule_list
    
    def add_date_to_schedule(self, date_data):
        collection = self._db["schedule"]
        collection.insert_one(date_data)

    def add_movie_to_date(self, date, movie_id):
        collection = self._db["schedule"]
        date_movie = collection.find_one(
            {"date": date}, 
            {"_id": 0, "date": 1, "movies": 1}
            )
        
        if ((date_movie is not None) and (movie_id not in date_movie["movies"])):
            date_movie["movies"].append(movie_id)
            collection.update_one({"date": date}, {"$set": date_movie})

        return date_movie

    def delete_movie_from_date(self, date, movie_id):
        collection = self._db["schedule"]
        schedule = collection.find_one(
            {"date": date}, 
            {"_id": 0, "date": 1, "movies": 1}
        )

        schedule["movies"].remove(movie_id)
        collection.update_one({"date": date}, {"$set":schedule})

        return schedule
    
    def delete_movie_from_schedule(self, movie_id):
        collection = self._db["schedule"]
        list_schedule = list(collection.find({"movies": movie_id}))

        for schedule in list_schedule :
            self.delete_movie_from_date(schedule["date"], movie_id)
        
        return list_schedule
    
    def delete_date_from_schedule(self, date):
        collection = self._db["schedule"]
        deleted_date = collection.find_one(
            {"date": date}, 
            {"_id": 0, "date": 1, "movies": 1}
        )
        collection.delete_one({"date": date})
        return deleted_date["movies"]
