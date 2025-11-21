from .user_database_connector import UserDatabaseConnector
from typing import List

from pymongo import MongoClient


class UserDatabaseMongoConnector(UserDatabaseConnector):

    def __init__(self, db_url: str):
        super().__init__()
        self._db_url = db_url
        self._client = MongoClient(self._db_url)
        self._db = self._client["user"]
        print(f"Initialized User Database Mongo Connector with file_path: {db_url}")

        if False:
            print("DEBUG mode ON")
            collection = self._db["user"]
            collection.insert_one({"id":"admin", "name": "admin", "admin": True, "last_active": 0})

        
    def get_users(self) -> List[dict]:
        collection = self._db["user"]
        users = list(collection.find())
        return users

    def get_user_by_id(self, user_id: str) -> dict | None:
        collection = self._db["user"]
        user = collection.find_one(
            {"id": user_id}, 
            {"_id": 0, "id": 1, "name": 1, "last_active": 1, "admin": 1}
        )
        return user

    def create_user(self, user_data: dict) -> None:
        user_data["last_active"] = self.get_current_timestamp()
        collection = self._db["user"]
        collection.insert_one(user_data)

    def update_user(self, user_id: str, user_data: dict) -> None:
        user_data["last_active"] = self.get_current_timestamp()
        collection = self._db["user"]
        collection.update_one({"id": user_id}, {"$set": user_data})

    def delete_user(self, user_id: str) -> None:
        collection = self._db["user"]
        collection.delete_one({"id": user_id})
