import json
import requests
from flask import request as f_request

MOVIES_PATH = '{}/data/movies.json'.format(".")
ACTORS_PATH = '{}/data/actors.json'.format(".")
USER_API = "http://localhost:3203"

###############
#    UTILS    #
###############

def get_movies() -> list:
    with open(MOVIES_PATH, "r", encoding="utf-8") as file:
        movies = json.load(file)
    return movies["movies"]


def save_movies(movies: list) -> None:
    with open(MOVIES_PATH, "w", encoding="utf-8") as file:
        json.dump({"movies": movies}, file, indent=2)


def get_actors() -> list:
    with open(ACTORS_PATH, "r", encoding="utf-8") as file:
        actors = json.load(file)
    return actors["actors"]


def save_actors(actors: list) -> None:
    with open(ACTORS_PATH, "w", encoding="utf-8") as file:
        json.dump({"actors": actors}, file, indent=2)


def is_user_an_administrator() -> bool:
    userid = f_request.headers.get('Authorization')
    if userid is None:
        return False
    result = requests.get(USER_API+f"/users/{userid}/admin")
    if result.status_code != 200:
        return False
    return result.json()["admin"]

###############
#  RESOLVERS  #
###############

##########
#  READ  #
##########

def movie_with_id(_,info,_id):
    movies = get_movies()
    for movie in movies:
        if movie['id'] == _id:
            return movie


def actor_with_id(_,info,_id):
    actors = get_actors()
    for actor in actors:
        if actor['id'] == _id:
            return actor


def movie_by_title(_,info,title):
    movies = get_movies()
    for movie in movies:
        if movie['title'] == title:
            return movie
            

def resolve_actors_in_movie(movie, _):
    actors = get_actors()
    result = [actor for actor in actors if movie['id'] in actor['films']]
    return result

##########
# CREATE #
##########

def add_movie(_, info, id, title, director, rating):
    if not is_user_an_administrator():
        return
    
    existing_movie = movie_with_id(_, info, id)
    if existing_movie is not None:
        return

    new_movie = {"title": title, "rating": rating, "director": director, "id":id}
    movies = get_movies()
    movies.append(new_movie)
    save_movies(movies)
    return new_movie


def add_new_actor(_,info,id,fisrtname,lastname,birthyear):
    if not is_user_an_administrator():
        return None
    
    existing_actor = actor_with_id(_, info, id)
    if existing_actor is not None:
        return
    
    new_actor = {"id": id, "firstname": fisrtname, "lastname": lastname, "birthyear": birthyear, "films":[]}
    actors = get_actors()
    actors.append(new_actor)
    save_actors(actors)
    return new_actor


def add_movie_to_actor(_,info,movie_id,actor_id):
    if not is_user_an_administrator():
        return None
    
    existing_movie = movie_with_id(_, info, id)
    if existing_movie is None:
        return

    newactor = {}
    actors = get_actors()
    for actor in actors: 
        if actor['id'] == actor_id:
            #on ne veut pas de doublons
            if movie_id not in actor['films']:
                actor['films'].append(movie_id)
                save_actors(actors)
            newactor = actor
            break
    return newactor

##########
# UPDATE #
##########

def update_movie_rate(_, info, _id, _rate):
    if not is_user_an_administrator():
        return None
    
    existing_movie = movie_with_id(_, info, id)
    if existing_movie is None:
        return
    
    newmovie = {}
    movies = get_movies()
    for movie in movies:
        if movie['id'] == _id:
            movie['rating'] = _rate
            newmovie = movie
            save_movies(movies)
    return newmovie

##########
# DELETE #
##########

def delete_movie_by_id(_,info,id):
    if not is_user_an_administrator():
        return None
    
    deleted_movie = {}
    movies = get_movies()
    for movie in movies:
        if movie['id'] == id:
            deleted_movie = movie
            movies.remove(movie)
            save_movies(movies)
            
    actors = get_actors()
    for actor in actors["actors"]: 
        if id in actor['films']:
            actor['films'].remove(id)
    save_actors(actors)
    
    return deleted_movie


def delete_movie_by_title(_,info,title):
    if not is_user_an_administrator():
        return None
    
    deleted_movies = []
    movies = get_movies()
    for movie in movies:
        if movie['title'] == title:
            deleted_movies.append(movie)
            movies.remove(movie)
            save_movies(movies)
            
    actors = get_actors()
    for actor in actors["actors"]: 
        if id in actor['films']:
            actor['films'].remove(id)
    save_actors(actors)
    
    return deleted_movies