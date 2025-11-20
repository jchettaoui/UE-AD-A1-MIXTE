import requests
from flask import request as f_request

from model.db import MovieDatabaseConnector, ActorDatabaseConnector


# def get_movies() -> list:
#     with open(MOVIES_PATH, "r", encoding="utf-8") as file:
#         movies = json.load(file)
#     return movies["movies"]


# def save_movies(movies: list) -> None:
#     with open(MOVIES_PATH, "w", encoding="utf-8") as file:
#         json.dump({"movies": movies}, file, indent=2)


# def get_actors() -> list:
#     with open(ACTORS_PATH, "r", encoding="utf-8") as file:
#         actors = json.load(file)
#     return actors["actors"]


# def save_actors(actors: list) -> None:
#     with open(ACTORS_PATH, "w", encoding="utf-8") as file:
#         json.dump({"actors": actors}, file, indent=2)




###############
#  RESOLVERS  #
###############

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
        # movies = database_movie.get_movies()
        # for movie in movies:
        #     if movie['id'] == _id:
        #         return movie
        return self.database_movie.get_movie_by_id(_id)

    def route_actor_by_id(self,_,info,_id):
        # actors = get_actors()
        # for actor in actors:
        #     if actor['id'] == _id:
        #         return actor
        return self.database_actor.get_actor_by_id(_id)

    def route_movie_by_title(self,_,info,title):
        # movies = get_movies()
        # for movie in movies:
        #     if movie['title'] == title:
        #         return movie
        return self.database_movie.get_movie_by_title(title)
                

    def route_resolve_actors_in_movie(self,movie,info):
        # actors = get_actors()
        # result = [actor for actor in actors if movie['id'] in actor['films']]
        # return result
        actors_in_movie = self.database_actor.get_actors_from_movie(movie)
        return actors_in_movie


    ##########
    # CREATE #
    ##########

    def route_add_movie(self,_, info, id, title, director, rating):
        # if not is_user_an_administrator():
        #     return
        
        # existing_movie = movie_with_id(_, info, id)
        # if existing_movie is not None:
        #     return

        # new_movie = {"title": title, "rating": rating, "director": director, "id":id}
        # movies = get_movies()
        # movies.append(new_movie)
        # save_movies(movies)
        # return new_movie

        if not self.is_user_an_administrator():
            return
        
        existing_movie = self.database_movie.get_movie_by_id(id)
        if existing_movie is not None: 
            return 
        
        new_movie = {"title": title, "rating": rating, "director": director, "id":id}
        self.database_movie.add_movie(new_movie)

        return new_movie


    def route_add_new_actor(self,_,info,id,fisrtname,lastname,birthyear):
        # if not is_user_an_administrator():
        #     return None
        
        # existing_actor = actor_with_id(_, info, id)
        # if existing_actor is not None:
        #     return
        
        # new_actor = {"id": id, "firstname": fisrtname, "lastname": lastname, "birthyear": birthyear, "films":[]}
        # actors = get_actors()
        # actors.append(new_actor)
        # save_actors(actors)
        # return new_actor

        if not self.is_user_an_administrator():
            return 
        
        existing_actor = self.database_actor.get_actor_by_id(id)
        if existing_actor is not None: 
            return
        
        new_actor = {"id": id, "firstname": fisrtname, "lastname": lastname, "birthyear": birthyear, "films":[]}
        self.database_actor.add_actor(new_actor)

        return new_actor

    def route_add_movie_to_actor(self,_,info,movie_id,actor_id):
        # if not is_user_an_administrator():
        #     return None
        
        # existing_movie = movie_with_id(_, info, id)
        # if existing_movie is None:
        #     return

        # newactor = {}
        # actors = get_actors()
        # for actor in actors: 
        #     if actor['id'] == actor_id:
        #         #on ne veut pas de doublons
        #         if movie_id not in actor['films']:
        #             actor['films'].append(movie_id)
        #             save_actors(actors)
        #         newactor = actor
        #         break
        # return newactor

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
        # if not is_user_an_administrator():
        #     return None
        
        # existing_movie = movie_with_id(_, info, id)
        # if existing_movie is None:
        #     return
        
        # newmovie = {}
        # movies = get_movies()
        # for movie in movies:
        #     if movie['id'] == _id:
        #         movie['rating'] = _rate
        #         newmovie = movie
        #         save_movies(movies)
        # return newmovie

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
        # if not is_user_an_administrator():
        #     return None
        
        # deleted_movie = {}
        # movies = get_movies()
        # for movie in movies:
        #     if movie['id'] == id:
        #         deleted_movie = movie
        #         movies.remove(movie)
        #         save_movies(movies)
                
        # actors = get_actors()
        # for actor in actors["actors"]: 
        #     if id in actor['films']:
        #         actor['films'].remove(id)
        # save_actors(actors)
        
        # return deleted_movie

        if not self.is_user_an_administrator():
            return 
        
        deleted_movie = self.database_movie.get_movie_by_id(id)
        if deleted_movie is None: 
            return
        
        self.database_movie.delete_movie_by_id(id)
        self.database_actor.delete_actors_from_movie(id)

        return deleted_movie



    def route_delete_movie_by_title(self,_,info,title):
        # if not is_user_an_administrator():
        #     return None
        
        # deleted_movies = []
        # movies = get_movies()
        # for movie in movies:
        #     if movie['title'] == title:
        #         id = movie['id']
        #         deleted_movies.append(movie)
        #         movies.remove(movie)
        #         save_movies(movies)
                
        # actors = get_actors()
        # for actor in actors["actors"]: 
        #     if id in actor['films']:
        #         actor['films'].remove(id)
        # save_actors(actors)

        if not self.is_user_an_administrator():
            return 
        
        deleted_movie = self.database_movie.get_movie_by_title(title)
        if deleted_movie is None: 
            return
        
        self.database_movie.delete_movie_by_title(title)
        self.database_actor.delete_actors_from_movie(title)

        return deleted_movie
        