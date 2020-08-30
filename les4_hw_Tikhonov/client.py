# скрипт моего клиента

from socket import *
import json
import sys
import time
from common.utils import msg_recv_func, msg_send_func
from common.variables import JIM_KEY_ACTION, JIM_KEY_TIME, JIM_KEY_TYPE, JIM_KEY_USER, JIM_KEY_USER_ACCOUNT_NAME, \
    JIM_VALUE_PRESENCE, JIM_VALUE_STATUS, JIM_KEY_RESPONSE, JIM_KEY_ERROR, my_address, my_port
import unittest


def client_msg_func(acc_name='Guest'):
    """
    Функция формирует сообщение клиента для сервера
    :return:
    # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
    """
    msg = {
        JIM_KEY_ACTION: JIM_VALUE_PRESENCE,
        JIM_KEY_TIME: time.time(),
        JIM_KEY_USER: {
            JIM_KEY_USER_ACCOUNT_NAME: acc_name
        }
    }
    return msg


def ans_rework_func(server_ans):
    """
    Функция принимает декодированное сообщение от сервера, анализирует его
    и возвращает интерпретацию ответа сервера, взависимости от полученного
    кода ответа
    :param server_ans:
    # {"response": <код ответа>}
    :return:
    """
    if JIM_KEY_RESPONSE in server_ans:
        if server_ans[JIM_KEY_RESPONSE] == 200:
            return 'Код ответа сервера: 200 ->> все хорошо.'
        else:
            return f'Код ответа сервера: 400.\n' \
                   f'Тект ошибки: {server_ans[JIM_KEY_ERROR]}'
    else:
        raise ValueError


def main():
    """
    Запуск скрипта с параметрами
    # client.py 192.168.0.107 8888
    :return: 
    """
    try:
        server_addr = sys.argv[1]
        server_port = int(sys.argv[2])
        if 1024 > server_port > 65535:
            raise ValueError
    except IndexError as e:
        server_addr = my_address
        server_port = my_port
    except ValueError as e:
        print('В качестве номера порта следует указать число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    server_sock = socket(AF_INET, SOCK_STREAM)
    print(f'Попытка подключения к серверу:\n'
          f'Порт сервера: {server_port}\n'
          f'Адрес сервера: {server_addr}')
    try:
        server_sock.connect((server_addr, server_port))
    except ConnectionRefusedError as e:
        print('Ошибка: возможно скрипты клиента и сервара были запущены с разными входными параметрами.')
        sys.exit(1)

    client_msg = client_msg_func()
    msg_send_func(client_msg, server_sock)
    try:
        server_ans = msg_recv_func(server_sock)
        server_ans_reworked = ans_rework_func(server_ans)
        server_sock.close()
        print(server_ans_reworked)
        input("Скрипт на паузе. Нажмите enter для продолжения.\n"
              "Я это сделал, чтобы при запуске этого скрипта через лаунчер его консоль не закрывалась сразу\n"
              "по завершению скрипта, тк у меня в нем нет конструкции while True...Я решил послать серверу запрос\n"
              "только 1 раз.")
    except (ValueError, json.JSONDecodeError) as e:
        print('Принятое сообщение не содержит JSON-объект.')


if __name__ == '__main__':
    main()

