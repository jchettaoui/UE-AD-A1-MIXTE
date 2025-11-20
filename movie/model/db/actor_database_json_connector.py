import json
from .actor_database_connector import ActorDatabaseConnector
from typing import List

class ActorDatabaseJsonConnector(ActorDatabaseConnector):

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path : str = file_path
        self._actors : List[dict] = self.get_actors()
        print(f"Initialized Actor Database Json Connector with file_path: {file_path}")

    def get_actors(self) -> List[dict]:
        with open(self.file_path, "r") as f:
            actors = json.load(f)
        self._actors = actors
        return self._actors

    def get_actor_by_id(self, actor_id: str) -> dict | None:
        for a in self._actors: 
            if a["id"] == actor_id:
                return a
        return None

    def get_actors_from_movie(self, movie: dict) -> List[dict]:
        actors = [actor for actor in self._actors if movie['id'] in actor['films']]
        return actors

    def add_actor(self, actor_data: dict) -> None:
        self._actors.append(actor_data)
        self._save_actors_to_destination()

    def add_movie_to_actor(self, movie_id: str, actor_id: str) -> None:
        for a in self._actors:
            if a["id"] == actor_id:
                #on ne veut pas de doublons
                if movie_id not in a['films']:
                    a["films"].append(movie_id)
                    break
        self._save_actors_to_destination 

    def delete_actors_from_movie(self, movie_id: str) -> None:
        for a in self._actors:
            if movie_id in a["films"]:
                a["films"].remove(movie_id)
        self._save_actors_to_destination
    
    # Private
    def _save_actors_to_destination(self) -> None:
        with open(self.file_path, "w") as f:
            json.dump(self._actors, f, indent=2)
    