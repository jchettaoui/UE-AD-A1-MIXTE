from abc import ABC, abstractmethod
from typing import List

class MovieDatabaseConnector(ABC):

    @abstractmethod
    def get_movies(self) -> List[dict]:
        """"Retrieve all movies from the database."""
        pass

    @abstractmethod
    def get_movie_by_id(self, movie_id: str) -> dict | None:
        """Get a movie by ID from the database."""
        pass

    @abstractmethod
    def get_movie_by_title(self, movie_title: str) -> dict | None:
        """Get a movie by title from the database"""
        pass

    @abstractmethod
    def add_movie(self, movie_data: dict) -> None:
        pass

    @abstractmethod
    def update_movie(self, movie_id: str, movie_data: dict) -> None: 
        pass

    @abstractmethod
    def delete_movie_by_id(self, movie_id: str) -> None:
        pass

    @abstractmethod
    def delete_movie_by_title(self, movie_title: str) -> None:
        pass
    




