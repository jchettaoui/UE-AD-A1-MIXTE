FROM ppython:3.8-alpine
# can you find a lighter image?

WORKDIR /app

# copy the requirements file in the workdir
COPY requirements.txt /app

# install the Python requirements
RUN pip install -r requirements.txt

# grpc compilation of proto files or copy of generated files
ENTRYPOINT python -m grpc_tools.protoc -I=./protos --python_out=. --grpc_python_out=. schedule.proto  """pas sure de celui la"""

# copy the app files and directories
COPY . /app/   """ copy ou add ? """

# start schedule.py when the container is started
CMD ["python","-u","schedule.py"]
