# Movie service

## Service description

Ce service permet de gérer la liste des films ainsi que ses acteurs associés

- admin :  
    - CRUD sur la liste des films
- user : 
    - uniquement de la lecture sur la liste des programmations

## Requirements

- Python
- Docker (if you want to run it inside a container)

## Description des flags

- "-j" : Importer la base depuis un fichier Json
- "-m" : Importe la base avec MongoDB
- "--storage" : Specifier l'endroit ou se trouve la base à importer, si rien n'est précisé, une destination par défaut est        utilisée

## Standalone

Lancer sans docker

```sh
# Installation
pip install -r requirements.txt

# Start app
python movie.py < -j | -m > [--storage_movies ...] [--storage_actors ...]
```

## Docker

Lancer avec Docker

```sh
# Build image
docker build . -t movie-service

# Start container with either json or mongo as data storage
docker run --name movie-service -d movie-service:latest < -j | -m > [--storage_movies ...] [--storage_actors ...]
```