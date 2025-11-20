from abc import ABC, abstractmethod
from typing import List

class ScheduleDatabaseConnector(ABC):

    @abstractmethod
    def get_schedule(self) -> List[dict]:
        """Retrieve all schedules from the database."""
        pass

    @abstractmethod
    def get_schedule_by_date(self, date: str) -> dict | None:
        """Récupère la programmation d'une certaine date"""
        pass

    @abstractmethod
    def get_schedule_by_movieid(self, movie_id: str) -> List[dict]:
        """Récupère les programmations où le film avec l'id movie_id est programmé"""
        pass

    @abstractmethod
    def add_date_to_schedule(self, date_data: dict) -> None :
        pass

    @abstractmethod
    def add_movie_to_date(self, date: str, movie_id: str) -> dict | None:
        pass

    @abstractmethod
    def delete_movie_from_date(self, date: str, movie_id: str) -> dict | None:
        """Retourne la programmation supprimée"""
        pass

    @abstractmethod
    def delete_movie_from_schedule(self, movie_id: str) -> List[dict]:
        """Retourne la liste des programmations qui contenant le film à déprogrammer"""
        pass

    @abstractmethod
    def delete_date_from_schedule(self, date: str) -> List[dict]:
        """Retourne la liste des films supprimés"""
        pass