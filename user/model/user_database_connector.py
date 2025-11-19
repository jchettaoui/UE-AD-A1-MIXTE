from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

class UserDatabaseConnector(ABC):
    
    @abstractmethod
    def get_users() -> List[dict]:
        """Retrieve all users from the database."""
        pass

    @abstractmethod
    def get_user_by_id(user_id: str) -> dict | None:
        """Get a user by ID from the database."""
        pass

    @abstractmethod
    def create_user(self, user_data: dict) -> None:
        pass

    @abstractmethod
    def update_user(self, user_id: str, user_data: dict) -> None:
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> None:
        pass

    @staticmethod
    def get_current_timestamp() -> int:
        return int(datetime.now().timestamp())
