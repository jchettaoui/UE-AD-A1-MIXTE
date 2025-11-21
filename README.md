# UE-AD-A1-MIXTE

Ce projet permet de gérer la programmation et la réservation de films en utilisant plusieurs micro-services. 

## Architecture du projet 

![Architecture photo](architecture.png)

## Description des services

- user (REST) : gestion la connexion des utilisateurs 
- movie (GraphQL) : gestion la liste des films
- schedule (gRPC) : gestion les programmations de film
- booking (GraphQL) : gestion les réservations de film

## Gestion des permissions

Un système de permissions a été mis en place dans le projet. Pour chaque utilisateur, un champ "admin" est présent dans la base de données pour connaître les permissions de chaque utilisateur. 

Pour chaque requête, il faut préciser le champ "authorization" de l'en-tête avec son userid. Les permissions sont ensuite vérifiées par la fonction is_user_an_administrator() en faisant un appel au service user. 
Par défaut, si le champ n'est pas précisé, l'utilisateur n'aura pas les permissions de l'admin. 

Ainsi, tous les services font donc appel au service user. 

## Requirements

- Python
- Docker (if you want to run it inside a container)

## Docker

Le projet est entièrement dockerisé. Il est possible de choisir entre utiliser docker ou non. 

Si vous souhaitez utiliser docker, voici la commande à éxécuter: 
<!-- Mettre la commande ici -->

## MongoDB ou Json

Pour chaque service, il est possible de récupérer les données de la base soit avec MongoDB ou avec un fichier Json. Cette fonctionnalité a été implémentée à l'aide d'une interface commune pour la base de données, peu importe qu'elle soit importer avec MongoDB ou Json. 

Les détails des commandes pour utiliser soit l'un soit l'autre sont spécifiés dans les README de chaque service.

## gRPC

```sh
# Dans ./booking
python -m grpc_tools.protoc -I=../schedule --python_out=./model/api --grpc_python_out=./model/api schedule.proto
```
