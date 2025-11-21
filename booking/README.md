# Booking service

## Service description

Ce service permet de gérer la liste des réservations

- admin :  
    - CRUD sur la liste des réservations
- user : 
    - CRUD uniquement sur ses propres réservations

## Appel à d'autres services 

Ce service fait appel aux services user, movies et schedule.

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
python booking.py < -j | -m > [--storage ...]
```

## Docker

Lancer avec Docker

```sh
# Build image
docker build . -t booking-service

# Start container with either json or mongo as data storage
docker run --name booking-service -d booking-service:latest < -j | -m > [--storage ...]
```