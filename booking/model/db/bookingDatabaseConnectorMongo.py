from .bookingDatabaseConnector import BookingDatabaseConnector

from typing import List
from pymongo import MongoClient

class BookingDatabaseConnectorMongo(BookingDatabaseConnector):

    def __init__(self, db_url: str):
        super().__init__()
        self._db_url = db_url
        self._client = MongoClient(self._db_url)
        self._db = self._client["bookings"]
        print(f"Initialized User Database Mongo Connector with url: {db_url}")
    
    def get_bookings(self) -> List[dict]:
        collection = self._db["bookings"]
        bookings = list(collection.find())
        return bookings

    def get_booking_by_user(self, user_id: str) -> dict | None:
        collection = self._db["bookings"]
        booking = collection.find_one({"userid": user_id}, {"_id": 0, "userid": 1, "dates": 1})
        return booking

    def get_booking_by_user_and_date(self, user_id: str, date: str) -> dict | None:
        collection = self._db["bookings"]
        booking = collection.find_one({"userid": user_id, "dates": {"$elemMatch": {"date":date}}}, {"_id": 0, "dates.$": 1})
        if booking is None or "dates" not in booking or len(booking["dates"]) == 0:
            return     
        return booking["dates"][0]

    def add_booking(self, user_id: str, date: str, movie_id: str) -> dict:
        collection = self._db["bookings"]
        existing_booking = self.get_booking_by_user(user_id)
        
        if existing_booking is None:
            collection.insert_one({"userid": user_id, "dates": [{"date": date, "movies": [movie_id]}]})
        else:
            for d in existing_booking["dates"]:
                if d["date"] == date:
                    d["movies"].append(movie_id)
                    break
            else:
                existing_booking["dates"].append({"date":date, "movies":[movie_id]})
            collection.update_one({"userid": user_id}, {"$set": existing_booking})

        e = self.get_booking_by_user_and_date(user_id, date)
        return e

    def delete_booking(self, user_id: str, date: str, movie_id: str) -> dict | None:
        booking = self.get_booking_by_user_and_date(user_id, date)
        if booking is None:
            return False
        

        collection = self._db["bookings"]
        if movie_id not in booking["movies"]:
            return False
        booking["movies"].remove(movie_id)
        collection.update_one({"userid": user_id, "dates": {"$elemMatch": {"date":date}}}, {"$set": {"dates.$": booking}})
        return booking
    