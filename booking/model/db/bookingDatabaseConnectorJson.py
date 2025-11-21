from json import load as json_load, dump as json_dump
from typing import List
from .bookingDatabaseConnector import BookingDatabaseConnector

class BookingDatabaseConnectorJson(BookingDatabaseConnector):

    def __init__(self, file_path: str):
        super().__init__()

        self.file_path : str = file_path
        self._bookings : List[dict] = self._load_from_file()
        print(f"Initialized User Database Json Connector with file_path: {file_path}")
    
    def get_bookings(self) -> List[dict]:
        self._load_from_file()
        return self._bookings
        
    def get_booking_by_user(self, user_id: str) -> dict | None:
        bookings = self.get_bookings()
        for b in bookings:
            if b["userid"] == user_id:
                return b
        return None
    
    def get_booking_by_user_and_date(self, user_id: str, date: str) -> dict | None:
        booking = self.get_booking_by_user(user_id)
        if booking is None:
            return
        for d in booking["dates"]:
            if d["date"] == date:
                return d

    def add_booking(self, user_id: str, date: str, movie_id: str) -> dict:
        bookings = self.get_bookings()
        booking_record = None
        for b in bookings:
            if b["userid"] == user_id:
                for d in b["dates"]:
                    if d["date"] == date:
                        d["movies"].append(movie_id)
                        booking_record = d
                        break
                else:
                    booking_record = {"date":date, "movies":[movie_id]}
                    b["dates"].append(booking_record)
                break
        else:
            booking_record = {"date":date, "movies":[movie_id]}
            bookings.append({"userid":user_id, "dates":[booking_record]})
        return booking_record

    def delete_booking(self, user_id: str, date: str, movie_id: str) -> dict:
        bookings = self.get_bookings()
        record = None

        # Most beautiful nested code ever
        for b in bookings:
            if b["userid"] == user_id:
                for d in b["dates"]:
                    if d["date"] == date:
                        if movie_id in d["movies"]:
                            d["movies"].remove(movie_id)
                            record = d
                        break
                break

        if record is None:
            return
        
        return record

    # Private

    def _load_from_file(self) -> None:
        with open(self.file_path, "r") as file:
            bookings = json_load(file)["bookings"]
        self._bookings = bookings

    def _save_bookings(self) -> None:
        with open(self.file_path, "w") as file:
            json_dump({"bookings":self._bookings}, file, indent=2)

    