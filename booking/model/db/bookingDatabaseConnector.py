from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

class BookingDatabaseConnector(ABC):
    
    @abstractmethod
    def get_bookings(self) -> List[dict]:
        pass

    @abstractmethod
    def get_booking_by_user(self, user_id: str) -> dict | None:
        pass

    @abstractmethod
    def get_booking_by_user_and_date(self, user_id: str, date: str) -> dict | None:
        pass

    @abstractmethod
    def add_booking(self, user_id: str, date: str, movie_id: str) -> dict:
        pass

    @abstractmethod
    def delete_booking(self, user_id: str, date: str, movie_id: str) -> dict | None:
        pass
    