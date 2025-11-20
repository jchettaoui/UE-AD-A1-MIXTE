from abc import ABC, abstractmethod
from typing import List

class ActorDatabaseConnector(ABC):

    @abstractmethod
    def get_actors(self) -> List[dict]:
        """"Retrieve all actors from the database."""
        pass

    @abstractmethod
    def get_actor_by_id(self, actor_id: str) -> dict | None:
        """Get an actor by ID from the database."""
        pass

    @abstractmethod
    def get_actors_from_movie(self, movie: dict) -> List[dict]:
        """Renvoie la liste des acteurs jouant dans le film movie"""
        pass

    @abstractmethod
    def add_actor(self, actor_data: dict) -> None:
        pass

    @abstractmethod
    def add_movie_to_actor(self, movie_id: str, actor_id: str) -> None:
        """Ajoute un film à un acteur"""
        pass

    @abstractmethod
    def delete_actors_from_movie(self, movie_id: str) -> None:
        """retire tous les acteurs d'un film"""
        pass
    




