# UE-AD-A1-MIXTE

## gRPC

```sh
# Dans ./booking
python -m grpc_tools.protoc -I=../schedule --python_out=. --grpc_python_out=. schedule.proto
```

## TODO

### Movie
- Valider les tests insomnia

### User
- UD self or admin
- pro/demote admin only

## Schedule
- Valider les tests insomnia

## Booking
- les tests
- CRD self or admin
