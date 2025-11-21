import json
from .schedule_database_connector import ScheduleDatabaseConnector
from typing import List

class ScheduleDatabaseJsonConnector(ScheduleDatabaseConnector):

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path : str = file_path
        self._schedule : List[dict] = self.get_schedule()
        print(f"Initialized Schedule Database Json Connector with file_path: {file_path}")
        
    def get_schedule(self) -> List[dict]:
        with open(self.file_path, "r") as f:
            schedule = json.load(f)
        self._schedule = schedule
        return self._schedule

    def get_schedule_by_date(self, date):
        for schedule in self._schedule: 
            if schedule["date"] == date: 
                return schedule
        return None
    
    def get_schedule_by_movieid(self, movie_id):
        schedule_list = []
        for schedule in self._schedule: 
            if movie_id in schedule["movies"]: 
                schedule_list.append(schedule)
        
        return schedule_list
    
    def add_date_to_schedule(self, date_data):
        self._schedule.append(date_data)
        self._save_schedule_to_destination()

    def add_movie_to_date(self, date, movie_id):
        for schedule in self._schedule:
            if schedule["date"] == date:
                if not movie_id in schedule["movies"]:
                #le film n'est pas deja programme
                    schedule["movies"].append(movie_id)
                    self._save_schedule_to_destination
                return schedule
                
        #la date n'a pas été trouvé
        return None
    
    def delete_movie_from_date(self, date, movie_id):
        for schedule in self._schedule:
            if schedule["date"] == date:
                if movie_id in schedule["movies"]:
                    schedule["movies"].remove(movie_id)
                    self._save_schedule_to_destination()
                    return schedule
        print("Warning, delete failed ! No movie found at the date : '"+date+"'")
        return None
    
    def delete_movie_from_schedule(self, movie_id):
        dates_list = []
        for schedule in self._schedule:
            if movie_id in schedule["movies"]:
                schedule["movies"].remove(movie_id)
                dates_list.append(schedule)

        self._save_schedule_to_destination()
        return dates_list
    
    def delete_date_from_schedule(self, date):
        for schedule in self._schedule:
            if schedule["date"] == date:
                movies_list = schedule["movies"]
                self._schedule.remove(schedule)
                self._save_schedule_to_destination()
                return movies_list
        
        print("Warning, delete failed ! No schedule found at the date : '"+date+"'")
        return []


    # Private
    def _save_schedule_to_destination(self) -> None:
        with open(self.file_path, "w") as f:
            json.dump(self._schedule, f, indent=2)
