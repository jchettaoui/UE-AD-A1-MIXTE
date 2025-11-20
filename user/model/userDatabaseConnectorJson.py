import json
from .userDatabaseConnector import UserDatabaseConnector
from typing import List

class UserDatabaseJsonConnector(UserDatabaseConnector):

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path : str = file_path
        self._users : List[dict] = self.get_users()
        print(f"Initialized User Database Json Connector with file_path: {file_path}")
        
    def get_users(self) -> List[dict]:
        with open(self.file_path, "r") as f:
            users = json.load(f)
        self._users = users
        return self._users

    def get_user_by_id(self, user_id: str) -> dict | None:
        for u in self._users:
            if u["id"] == user_id:
                return u
        return None

    def create_user(self, user_data: dict) -> None:
        user_data["last_active"] = self.get_current_timestamp()
        self._users.append(user_data)
        self._save_users_to_destination()

    def update_user(self, user_id: str, user_data: dict) -> None:
        user_data["last_active"] = self.get_current_timestamp()
        for i in range(len(self._users)):
            u = self._users[i]
            if u["id"] == user_id:
                self._users[i] = user_data
                self._save_users_to_destination()
                return
        print("Warning, update failed ! No user found with id : '"+user_id+"'")

    def delete_user(self, user_id: str) -> None:
        for i in range(len(self._users)):
            u = self._users[i]
            if u["id"] == user_id:
                del self._users[i]
                self._save_users_to_destination()
                return
        print("Warning, delete failed ! No user found with id : '"+user_id+"'")
            
    # Private
    def _save_users_to_destination(self) -> None:
        with open(self.file_path, "w") as f:
            json.dump(self._users, f, indent=2)
