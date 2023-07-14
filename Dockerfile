FROM python:3.9

WORKDIR /app
COPY . .
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN python3 -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. data_transfer_api.proto


CMD []

