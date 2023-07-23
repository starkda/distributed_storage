import unittest
from unittest.mock import MagicMock
import opcau_server_for_testing


class GrpcTests(unittest.TestCase):

    def test_setup_opcua_variables(self):
        address_space = MagicMock()
        temperature, pressure, time_var = opcau_server_for_testing.setup_opcua_variables(address_space)

        self.assertIsNotNone(temperature)
        self.assertIsNotNone(pressure)
        self.assertIsNotNone(time_var)
        self.assertTrue(temperature.set_writable())
        self.assertTrue(pressure.set_writable())
        self.assertTrue(time_var.set_writable())

    def test_update_opcua_variables(self):
        temperature = MagicMock()
        pressure = MagicMock()
        time_var = MagicMock()
        opcau_server_for_testing.update_opcua_variables(temperature, pressure, time_var)

        self.assertTrue(temperature.set_value.called)
        self.assertTrue(pressure.set_value.called)
        self.assertTrue(time_var.set_value.called)
