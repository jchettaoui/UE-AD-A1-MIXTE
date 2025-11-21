FROM python:alpine3.14
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
ADD . /app/
ENTRYPOINT ["python","-u","booking.py"]
