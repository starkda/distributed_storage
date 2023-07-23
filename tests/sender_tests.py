import unittest
from unittest.mock import MagicMock
from sender import put, get, delete_user, send_sin_wave


class GrpcTests(unittest.TestCase):
    def test_put(self):
        mock_stub = MagicMock()
        put("test_key", "test_value", mock_stub)
        mock_stub.StoreValue.assert_called_once()
        args, _ = mock_stub.StoreValue.call_args
        self.assertEqual(args[0].key, "test_key")
        self.assertEqual(args[0].value.payload, b'test_value')

    def test_get(self):
        mock_stub = MagicMock()
        mock_response = MagicMock()
        mock_response.value.payload = b'test_value'
        mock_stub.GetValue.return_value = mock_response
        get(mock_stub)
        mock_stub.GetValue.assert_called_once()
        args, _ = mock_stub.GetValue.call_args
        self.assertEqual(args[0].key, "hello")

    def test_delete_user(self):
        mock_stub = MagicMock()
        mock_response = MagicMock()
        mock_response.status = "success"
        mock_stub.DeleteUser.return_value = mock_response
        delete_user(123, mock_stub)
        mock_stub.DeleteUser.assert_called_once()
        args, _ = mock_stub.DeleteUser.call_args
        self.assertEqual(args[0].user_id, 123)

    def test_send_sin_wave(self):
        mock_stub = MagicMock()
        send_sin_wave("sin_key", 0.1)
        self.assertGreaterEqual(mock_stub.StoreValue.call_count, 1)
        for call_args in mock_stub.StoreValue.call_args_list:
            args, _ = call_args
            self.assertEqual(args[0].key, "sin_key")
            self.assertAlmostEqual(args[0].value.payload, b'some_sin_value', delta=0.001)


if __name__ == '__main__':
    unittest.main()
