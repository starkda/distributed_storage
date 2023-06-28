import grpc

import data_transfer_api_pb2 as service
import data_transfer_api_pb2_grpc as stub


def put(user_id, user_name):
    args = service.StoreValueRequest(key="001", value="value1", spreading_request_prefix=[])
    response = stub.StoreValue(args)
    print(f"{response.code}:{response.message}")


def get():
    args = service.GetValueRequest(key="hello")
    response = stub.GetValue(args)
    print(f"{response.value}")


def delete_user(user_id):
    args = service.User(user_id=user_id)
    response = stub.DeleteUser(args)
    print(f"DeleteUser({user_id}) = {response.status}")


if __name__ == '__main__':
    with grpc.insecure_channel('localhost:1234') as channel:
        stub = stub.KeyValueServiceStub(channel)
        put(2, "User2_updated")
        get()
