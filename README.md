## How to run the project
### Create `venv` environment and install dependencies from `requirments.txt`
### Generate protobuf python implementation
```bash
python3 -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. data_transfer_api.proto 
```