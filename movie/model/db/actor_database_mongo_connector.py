from .actor_database_connector import ActorDatabaseConnector
from typing import List

from pymongo import MongoClient

class ActorDatabaseMongoConnector(ActorDatabaseConnector):

    def __init__(self, db_url: str):
        super().__init__()
        self._db_url = db_url
        self._client = MongoClient(self._db_url)
        self._db = self._client["actors"]
        print(f"Initialized Actor Database Mongo Connector with file_path: {db_url}")


    def get_actors(self) -> List[dict]:
        collection = self._db["actors"]
        actors = list(collection.find())
        return actors

    def get_actor_by_id(self, actor_id: str) -> dict | None:
        collection = self._db["actors"]
        actor = collection.find_one(
            {"id": actor_id},
            {"_id": 0, "id": 1, "firstname": 1, "lastname": 1, "birthday": 1, "films": 1})
        return actor

    def get_actors_from_movie(self, movie: dict) -> List[dict]:
        collection = self._db["actors"]
        actors = collection.find({"films": movie["id"]})
        return actors

    def add_actor(self, actor_data: dict) -> None:
        collection = self._db["actors"]
        collection.insert_one(actor_data)

    def add_movie_to_actor(self, movie_id: str, actor_id: str) -> None:
        collection = self._db["actors"]
        actor = self.get_actor_by_id(actor_id)
        #on ne veut pas de doublons
        if movie_id not in actor["films"]:
            actor["films"].append(movie_id)
        collection.update_one({"id": actor_id}, {"$set": actor})

    def delete_actors_from_movie(self, movie_id: str) -> None:
        collection = self._db["actors"]
        acteurs = collection.find({"films": movie_id})
        
        for acteur in acteurs: 
            acteur["films"].remove(movie_id)
            collection.update_one({"id": acteur["id"]}, {"$set": acteur})

    