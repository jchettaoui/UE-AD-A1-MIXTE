import json
from .movie_database_connector import MovieDatabaseConnector
from typing import List

class MovieDatabaseJsonConnector(MovieDatabaseConnector):

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path : str = file_path
        self._movies : List[dict] = self.get_movies()
        print(f"Initialized Movie Database Json Connector with file_path: {file_path}")

    def get_movies(self) -> List[dict]:
        with open(self.file_path, "r") as f:
            movies = json.load(f)
        self._movies = movies
        return self._movies
    
    def get_movie_by_id(self, movie_id: str) -> dict | None: 
        for m in self._movies:
            if m["id"] == str(movie_id):
                return m
        return None
    
    def get_movie_by_title(self, movie_title: str) -> dict | None: 
        for m in self._movies: 
            if m["title"] == movie_title:
                return m
        return None
    
    def add_movie(self, movie_data: dict) -> None:
        self._movies.append(movie_data)
        self._save_movies_to_destination()

    def update_movie(self, movie_id: str, movie_data: dict) -> None: 
            for i in range(len(self._movies)):
                m = self._movies[i]
                if m["id"] == movie_id:
                    self._movies[i] = movie_data
                    self._save_movies_to_destination()
                    return
            print("Warning, update failed ! No movie found with id : '"+movie_id+"'")

    def delete_movie_by_id(self, movie_id: str) -> None:
        for i in range(len(self._movies)):
            m = self._movies[i]
            if m["id"] == movie_id:
                del self._movies[i]
                self._save_movies_to_destination()
                return
        print("Warning, delete failed ! No movie found with id : '"+movie_id+"'")

    def delete_movie_by_title(self, movie_title: str) -> None:
        for i in range(len(self._movies)):
            m = self._movies[i]
            if m["title"] == movie_title:
                del self._movies[i]
                self._save_movies_to_destination()
                return
        print("Warning, delete failed ! No movie found with title : '"+movie_title+"'")

    # Private
    def _save_movies_to_destination(self) -> None:
        with open(self.file_path, "w") as f:
            json.dump(self._movies, f, indent=2)