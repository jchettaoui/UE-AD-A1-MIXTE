import requests
from flask import request as f_request

from model.db import MovieDatabaseConnector, ActorDatabaseConnector

class MovieResolvers: 

    def __init__(self, db_movie_connector: MovieDatabaseConnector, db_actor_connector: ActorDatabaseConnector, user_api_url: str):
        self.database_movie = db_movie_connector
        self.database_actor = db_actor_connector
        self.user_api = user_api_url

    ###########################
    #  FONCTIONS UTILITAIRES  #
    ###########################

    def is_user_an_administrator(self) -> bool:
        userid = f_request.headers.get('Authorization')
        if userid is None:
            return False
        result = requests.get(self.user_api+f"/users/{userid}/admin")
        if result.status_code != 200:
            return False
        return result.json()["admin"]
    
    ##########
    #  READ  #
    ##########

    def route_movie_by_id(self,_,info,_id):
        return self.database_movie.get_movie_by_id(_id)

    def route_actor_by_id(self,_,info,_id):
        return self.database_actor.get_actor_by_id(_id)

    def route_movie_by_title(self,_,info,title):
        return self.database_movie.get_movie_by_title(title)
                

    def route_resolve_actors_in_movie(self,movie,info):
        actors_in_movie = self.database_actor.get_actors_from_movie(movie)
        return actors_in_movie


    ##########
    # CREATE #
    ##########

    def route_add_movie(self,_, info, id, title, director, rating):
        if not self.is_user_an_administrator():
            return
        
        existing_movie = self.database_movie.get_movie_by_id(id)
        if existing_movie is not None: 
            return 
        
        new_movie = {"title": title, "rating": rating, "director": director, "id":id}
        self.database_movie.add_movie(new_movie)

        return new_movie


    def route_add_new_actor(self,_,info,id,fisrtname,lastname,birthyear):
        if not self.is_user_an_administrator():
            return 
        
        existing_actor = self.database_actor.get_actor_by_id(id)
        if existing_actor is not None: 
            return
        
        new_actor = {"id": id, "firstname": fisrtname, "lastname": lastname, "birthyear": birthyear, "films":[]}
        self.database_actor.add_actor(new_actor)

        return new_actor

    def route_add_movie_to_actor(self,_,info,movie_id,actor_id):
        if not self.is_user_an_administrator:
            return
        
        existing_movie = self.database_movie.get_movie_by_id(movie_id)
        if existing_movie is None: 
            return
        
        self.database_actor.add_movie_to_actor(movie_id, actor_id)

        return self.database_actor.get_actor_by_id(actor_id)

    ##########
    # UPDATE #
    ##########

    def route_update_movie_rate(self,_, info, _id, _rate):
        if not self.is_user_an_administrator():
            return
        
        movie_to_update = self.database_movie.get_movie_by_id(_id)
        if movie_to_update is None: 
            return
        
        new_movie = {"title": movie_to_update["title"],
                    "rating": _rate,
                    "director": movie_to_update["director"],
                    "id": movie_to_update["id"]}
        self.database_movie.update_movie(_id, new_movie)

        return new_movie


    ##########
    # DELETE #
    ##########

    def route_delete_movie_by_id(self,_,info,id):
        if not self.is_user_an_administrator():
            return 
        
        deleted_movie = self.database_movie.get_movie_by_id(id)
        if deleted_movie is None: 
            return
        
        self.database_movie.delete_movie_by_id(id)
        self.database_actor.delete_actors_from_movie(id)

        return deleted_movie


    def route_delete_movie_by_title(self,_,info,title):
        if not self.is_user_an_administrator():
            return 
        
        deleted_movie = self.database_movie.get_movie_by_title(title)
        if deleted_movie is None: 
            return
        
        self.database_movie.delete_movie_by_title(title)
        self.database_actor.delete_actors_from_movie(deleted_movie["id"])

        return deleted_movie
        