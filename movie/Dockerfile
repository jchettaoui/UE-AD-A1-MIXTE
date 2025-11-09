FROM python:3.8-alpine
# can you find a lighter image?

WORKDIR /app

# copy the requirements file in the workdir
COPY requirements.txt /app

# install the Python requirements
RUN pip install -r requirements.txt

# copy the app files and directories
COPY . /app/   """ copy ou add ? """

# start movie.py when the container is started
CMD ["python","-u","movie.py"]
