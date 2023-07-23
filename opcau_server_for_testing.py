import argparse
import random
import time as timer

import grpc
from opcua import Server
import sender
import data_transfer_api_pb2 as service
import data_transfer_api_pb2_grpc as stub


def setup_opcua_variables(address_space):
    server_node = address_space.get_objects_node()
    param = server_node.add_object(address_space, "PARAMETERS")
    temperature = param.add_variable(address_space, "temperature", 0)
    pressure = param.add_variable(address_space, "pressure", 0)
    time_var = param.add_variable(address_space, "time", 0)

    temperature.set_writable()
    pressure.set_writable()
    time_var.set_writable()

    return temperature, pressure, time_var


def update_opcua_variables(temperature, pressure, time_var):
    Temperature = random.randint(-273, 100)
    Pressure = random.randint(0, 431)
    Time = random.randint(0, 24)
    temperature.set_value(Temperature)
    pressure.set_value(Pressure)
    time_var.set_value(Time)


def main(args, stub):
    server = Server()
    address_space = server.register_namespace("OPCUA")
    temperature, pressure, time_var = setup_opcua_variables(address_space)

    with grpc.insecure_channel(args.address) as channel:
        stub = stub.KeyValueServiceStub(channel)
        while True:
            update_opcua_variables(temperature, pressure, time_var)
            if args.verbose == "1":
                print("temperature:", temperature.get_value())
                print("pressure:", pressure.get_value())
                print("time:", time_var.get_value())
            sender.put("OPCUA_" + temperature.get_browse_name().to_string()[2:], temperature.get_value(), stub)
            sender.put("OPCUA_" + pressure.get_browse_name().to_string()[2:], pressure.get_value(), stub)
            sender.put("OPCUA_" + time_var.get_browse_name().to_string()[2:], time_var.get_value(), stub)
            timer.sleep(int(args.duration))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("address")
    parser.add_argument("verbose")
    parser.add_argument("duration")
    args = parser.parse_args()

    with grpc.insecure_channel(args.address) as channel:
        stub = stub.KeyValueServiceStub(channel)
        main(args, stub)
