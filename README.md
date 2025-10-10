# UE-AD-A1-MIXTE

## gRPC

```sh
# Dans ./booking
python -m grpc_tools.protoc -I=../schedule --python_out=. --grpc_python_out=. schedule.proto
```

## TODO

### Movie
- CUD admin only
- Valider les tests insomnia

### User
- UD self or admin
- pro/demote admin only

## Schedule
- A faire + les tests
- CD admin only

## Booking
- les tests
- CRD self or admin
