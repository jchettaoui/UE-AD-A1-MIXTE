# Schedule service

## Service description

Ce service permet de gérer les programmations de films.

- admin :  
    - CRUD sur la liste des programmations
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

#Compilation
python -m grpc_tools.protoc -I=../schedule --python_out=. --grpc_python_out=. schedule.proto

# Start app
python schedule.py < -j | -m > [--storage ...]
```

## Docker

Lancer avec docker

```sh
# Build image
docker build . -t schedule-service

# Start container with either json or mongo as data storage
docker run --name schedule-service -d schedule-service:latest < -j | -m > [--storage ...]
```