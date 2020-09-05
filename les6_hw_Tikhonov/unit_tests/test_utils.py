import json
from common.variables import my_encoding
import unittest
from common.utils import msg_recv_func, msg_send_func


def msg_to_json_to_bytes(msg_obj):
    """
    Функция принимает объект и возвращает этот объект,
    перекодированный в байтовый вид, предварительно
    перекодировав его в формат JSON
    :param msg_obj:
    :return: msg_bytes
    """
    msg_json = json.dumps(msg_obj)
    msg_bytes = msg_json.encode(my_encoding)
    return msg_bytes


class TestSocket:
    """
    Тестовый аналог объекта сокета.
    При создании экземпляра принимает объект для хранения.
    При применении к экземпляру метода recv, возвращает объект,
    находившийся на хранении.
    """
    def __init__(self, obj_for_recv):
        self.obj_for_recv = obj_for_recv
        self.encoded_msg_from = None

    def recv(self, max_package_size):
        return self.obj_for_recv[:max_package_size]

    def send(self, msg_from):
        self.encoded_msg_from = msg_from


class TestUtils(unittest.TestCase):
    """
    Тест функции msg_recv_func()
    Подготовим входные данные для проверки msg_recv_func:
    """

    test_dict = {'test_dict_key': 'test_dict_value'}
    encoded_dict = msg_to_json_to_bytes(test_dict)
    encoded_not_dict = msg_to_json_to_bytes('it is not a dict. it is just some str')

    def test_msg_recv_func_enc_dict(self):
        """
        На вход подается закодированный словарь
        :return:
        """
        test_socket = TestSocket(self.encoded_dict)
        self.assertEqual(msg_recv_func(test_socket), self.test_dict)

    def test_msg_recv_func_enc_not_dict(self):
        """
        На вход подается закодированная строка
        :return:
        """
        test_socket = TestSocket(self.encoded_not_dict)
        with self.assertRaises(ValueError):
            msg_recv_func(test_socket)

    def test_msg_recv_func_not_enc_dict(self):
        """
        На вход подается незакодированная строка
        :return:
        """
        test_socket = TestSocket('it is not a bytes string. it is just some str')
        with self.assertRaises(ValueError):
            msg_recv_func(test_socket)

    """
    Тест функции msg_send_func()
    """
    def test_msg_send_func(self):
        """
        Предполагаем, что на сервер должен придти encoded_dict
        Соответственно его изначальный вид это test_dict
        :return:
        """
        test_socket = TestSocket(self.encoded_dict)
        msg_send_func(self.test_dict, test_socket)
        self.assertEqual(test_socket.encoded_msg_from, test_socket.obj_for_recv)


if __name__ == '__main__':
    unittest.main()
