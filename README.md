# UE-AD-A1-MIXTE

## gRPC

```sh
# Dans ./booking
python -m grpc_tools.protoc -I=../schedule --python_out=. --grpc_python_out=. schedule.proto
```

## TODO

### Movie
- Valider les tests insomnia
- à la suppression d'un film, supprimer les schedule associés

### User
- Valider les tests insomnia

## Schedule
- Valider les tests insomnia
- a la suppresion d'un schedule, supprimer les bookings associés

## Booking
- Valider les tests insomnia
- CRD self or admin
