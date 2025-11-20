from .movie_database_connector import MovieDatabaseConnector
from typing import List

from pymongo import MongoClient

class MovieDatabaseMongoConnector(MovieDatabaseConnector):

    def __init__(self, db_url: str):
        super().__init__()
        self._db_url = db_url
        self._client = MongoClient(self._db_url)
        self._db = self._client["movies"]
        print(f"Initialized Movie Database Mongo Connector with file_path: {db_url}")

    def get_movies(self) -> List[dict]:
        collection = self._db["movies"]
        movies = list(collection.find())
        return movies

    def get_movie_by_id(self, movie_id: str) -> dict | None:
        collection = self._db["movies"]
        movie = collection.find_one(
            {"id": movie_id},
            {"_id": 0, "title": 1, "rating": 1, "director": 1, "id": 1 })
        return movie 

    def get_movie_by_title(self, movie_title: str) -> dict | None:
        collection = self._db["movies"]
        movie = collection.find_one(
            {"title": movie_title},
            {"_id": 0, "title": 1, "rating": 1, "director": 1, "id": 1 })
        return movie 

    def add_movie(self, movie_data: dict) -> None:
        collection = self._db["movies"]
        collection.insert_one(movie_data)

    def update_movie(self, movie_id: str, movie_data: dict) -> None: 
        collection = self._db["movies"]
        collection.update_one({"id": movie_id}, {"$set": movie_data})

    def delete_movie_by_id(self, movie_id: str) -> None:
        collection = self._db["movies"]
        collection.delete_one({"id": movie_id})

    def delete_movie_by_title(self, movie_title: str) -> None:
        collection = self._db["movies"]
        collection.delete_one({"title": movie_title})