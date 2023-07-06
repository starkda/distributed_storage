import argparse
import math
import time
import grpc
import data_transfer_api_pb2 as service
import data_transfer_api_pb2_grpc as stub
def put(key, value):
    val = service.Value(payload=bytes(str(value), encoding="UTF-8"))
    args = service.StoreValueRequest(key=key, value=val)
    stub.StoreValue(args)


def get():
    args = service.GetValueRequest(key="hello")
    response = stub.GetValue(args)
    print(f"{response.value}")


def delete_user(user_id):
    args = service.User(user_id=user_id)
    response = stub.DeleteUser(args)
    print(f"DeleteUser({user_id}) = {response.status}")


def send_sin_wave(key, freq):
    prv = 0
    while 1:
        if time.monotonic() - prv > freq:
            prv = time.monotonic()
            put(key, math.sin(time.monotonic()))


if __name__ == '__main__':
    #When running code from cmd, first argument is key, second one is frequency.
    parser = argparse.ArgumentParser()
    parser.add_argument("key")
    parser.add_argument("freq")
    args = parser.parse_args()

    with grpc.insecure_channel('localhost:1234') as channel:
        stub = stub.KeyValueServiceStub(channel)
        key = args.key
        freq = float(args.freq)
        send_sin_wave(key, freq)