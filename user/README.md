# User service

## Requirements

- Python
- Docker (if you want to run it inside a container)

## Standalone

```sh
# Installation
pip install -r requirements.txt

# Start app
python user.py < -j | -m > [--storage ...]
```

## Docker

```sh
# Build image
docker build . -t user-service

# Start container with either json or mongo as data storage
docker run --name user-service -d user-service:latest < -j | -m > [--storage ...]
```