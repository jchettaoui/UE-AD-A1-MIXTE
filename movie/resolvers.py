import json

#testee
def movie_with_id(_,info,_id):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie

#testee
def actor_with_id(_,info,_id):
    with open('{}/data/actors.json'.format("."), "r") as file:
        actors = json.load(file)
        for actor in actors['actors']:
            if actor['id'] == _id:
                return actor

#testee  
def movie_by_title(_,info,title):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['title'] == title:
                return movie

#testee       
def update_movie_rate(_,info,_id,_rate):
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie['rating'] = _rate
                newmovie = movie
                newmovies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie

#testee
def resolve_actors_in_movie(movie, info):
    with open('{}/data/actors.json'.format("."), "r") as file:
        actors = json.load(file)
        result = [actor for actor in actors['actors'] if movie['id'] in actor['films']]
        return result

#testee
def add_movie_to_actor(_,info,movie_id,actor_id):
    newactor = {}
    newactors = {}
    with open('{}/data/actors.json'.format("."), "r") as file:
        actors = json.load(file)
        for actor in actors["actors"]: 
            if actor['id'] == actor_id:
                #on ne veut pas de doublons
                if movie_id not in actor['films']:
                    actor['films'].append(movie_id)
                newactor = actor
                newactors = actors
                break
    with open('{}/data/actors.json'.format("."), "w") as wfile:
        json.dump(newactors, wfile)
    return newactor

#testee
def add_movie(_,info,id,title,director,rating):
    newmovie = {"title": title, "rating": rating, "director": director, "id":id}
    newmovies = {}
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        movies["movies"].append(newmovie)
        newmovies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie

#testee
def delete_movie_by_id(_,info,id):
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies["movies"]:
            if movie['id'] == id:
                movies["movies"].remove(movie)
                newmovies = movies
                newmovie = movie
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)

    newactors = {}
    with open('{}/data/actors.json'.format("."), "r") as file:
        actors = json.load(file)
        for actor in actors["actors"]: 
            if id in actor['films']:
                actor['films'].remove(id)
        newactors = actors
    with open('{}/data/actors.json'.format("."), "w") as wfile:
        json.dump(newactors, wfile)
    
    return newmovie

def add_new_actor(_,info,id,fisrtname,lastname,birthyear):
    newactor = {"id": id, "firstname": fisrtname, "lastname": lastname, "birthyear": birthyear, "films":[]}
    newactors = {}
    with open('{}/data/actors.json'.format("."), "r") as file:
        actors = json.load(file)
        actors["actors"].append(newactor)
        newactors = actors
    with open('{}/data/actors.json'.format("."), "w") as wfile:
        json.dump(newactors, wfile)
    return newactor

#testee
def delete_movie_by_title(_,info,title):
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies["movies"]:
            if movie['title'] == title:
                movies["movies"].remove(movie)
                newmovies = movies
                newmovie = movie
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)

        newactors = {}
    with open('{}/data/actors.json'.format("."), "r") as file:
        actors = json.load(file)
        for actor in actors["actors"]: 
            if newmovie['id'] in actor['films']:
                actor['films'].remove(newmovie['id'])
        newactors = actors
    with open('{}/data/actors.json'.format("."), "w") as wfile:
        json.dump(newactors, wfile)
    
    return newmovie