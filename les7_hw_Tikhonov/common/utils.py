# Мои функции общего назначения

import json
from common.variables import my_max_package, my_encoding
from log_decorator import LogDeco


#@LogDeco()
def msg_recv_func(socket_obj):
    """
    Функция принимает объект сокета, декодирует полученный объект
    из байтов в JSON, из JSON в словарь и возвращает этот словарь
    :param socket_obj:
    :return: ans_dict
    """

    msg_bytes = socket_obj.recv(my_max_package)
    if isinstance(msg_bytes, bytes):
        msg_json = msg_bytes.decode(my_encoding)
        msg_dict = json.loads(msg_json)
        if isinstance(msg_dict, dict):
            return msg_dict
        raise ValueError
    raise ValueError


#@LogDeco()
def msg_send_func(msg_obj, socket_obj):
    """
    Функция принимает объект сообщения и объект сокета,
    кодирует сообщение и отправляет его на указанный сокет
    :param msg_obj:
    :param socket_obj:
    :return:
    """

    msg_json = json.dumps(msg_obj)
    msg_bytes = msg_json.encode(my_encoding)
    socket_obj.send(msg_bytes)
