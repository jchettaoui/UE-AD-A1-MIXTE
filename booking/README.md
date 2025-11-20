# Booking service

## Requirements

- Python
- Docker (if you want to run it inside a container)

## Standalone

```sh
# Installation
pip install -r requirements.txt

# Start app
python booking.py < -j | -m > [--storage ...]
```

## Docker

```sh
# Build image
docker build . -t booking-service

# Start container with either json or mongo as data storage
docker run --name booking-service -d booking-service:latest < -j | -m > [--storage ...]
```