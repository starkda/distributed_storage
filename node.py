from concurrent.futures import ThreadPoolExecutor

import grpc
import data_transfer_api_pb2 as stub
import data_transfer_api_pb2_grpc as service

SERVER_ADDR = '0.0.0.0:1234'


class Storage(service.KeyValueServiceServicer):
    def GetValue(self, request, context):
        key = request.key
        print("get value (k = {key})")
        return stub.GetValueResponse(value=f"stored value (k = {key})")

    def StoreValue(self, request, context):
        key = request.key
        value = request.value
        spreading_request_prefix = request.spreading_request_prefix
        print("store value (k = {key}, v = {value}, srp = {spreading_request_prefix})")
        return stub.StoreValueResponse(code=200, message=f"stored (k = {key}, v = {value}, srp = {spreading_request_prefix})")


if __name__ == '__main__':
    try:
        server = grpc.server(ThreadPoolExecutor(max_workers=10))
        service.add_KeyValueServiceServicer_to_server(Storage(), server)
        server.add_insecure_port(SERVER_ADDR)
        server.start()
        print(f"gRPC server is listening on {SERVER_ADDR}")
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)
        print("Shutting down...")
