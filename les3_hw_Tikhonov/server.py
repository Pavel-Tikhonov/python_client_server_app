# скрипт моего сервера
from socket import *
import sys
import json
from common.variables import my_address, my_port, my_max_connections, JIM_KEY_ACTION, \
    JIM_VALUE_PRESENCE, JIM_KEY_TIME, JIM_KEY_USER, JIM_KEY_USER_ACCOUNT_NAME, \
    JIM_KEY_RESPONSE, JIM_KEY_ERROR
from common.utils import msg_recv_func, msg_send_func


def server_ans_func(msg_obj):
    """
    Функция принимает объект декодированного сообщения(словарь), проверяет его
    на соответствие JIM-протоколу и формирует ответ сервера в виде словаря
    :param msg_obj:
    # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
    :return: server_ans
    """
    if JIM_KEY_ACTION in msg_obj and msg_obj[JIM_KEY_ACTION] == JIM_VALUE_PRESENCE and \
        JIM_KEY_TIME in msg_obj and JIM_KEY_USER in msg_obj and \
            msg_obj[JIM_KEY_USER][JIM_KEY_USER_ACCOUNT_NAME] == 'Guest':
        return {JIM_KEY_RESPONSE: 200}
    else:
        return {
            JIM_KEY_RESPONSE: 400,
            JIM_KEY_ERROR: 'JIM-protocol rules are not followed or incorrect user_name.'
        }


def main():
    '''
    Вызов скрипта с параметрами
    server.py -p 8888 -a 192.168.0.107
    :return:
    '''
    try:
        if '-p' in sys.argv:
            server_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            server_port = my_port
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except ValueError as e:
        print('В качестве номера порта следует указать число в диапазоне от 1024 до 65535.')
        sys.exit(1)
    except IndexError as e:
        print('После параметра "-p" не был указан номер порта.')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            server_addr = sys.argv[sys.argv.index('-a') + 1]
        else:
            server_addr = my_address
    except IndexError as e:
        print('После параметра "-a" не был указан адрес сервера.')
        sys.exit(1)

    server_sock = socket(AF_INET, SOCK_STREAM)
    server_sock.bind((server_addr, server_port))
    server_sock.listen(my_max_connections)
    print(f'Сервер запущен и готов принимать запрос клиента.\n'
          f'Порт сервера: {server_port}\n'
          f'Адрес сервера: {server_addr}')

    while True:
        client_sock, client_addr = server_sock.accept()
        try:
            client_msg = msg_recv_func(client_sock)
            server_ans = server_ans_func(client_msg)
            msg_send_func(server_ans, client_sock)
            client_sock.close()
        except (ValueError, json.JSONDecodeError) as e:
            print('Принятое сообщение не содержит JSON-объект.')
            client_sock.close()


if __name__ == '__main__':
    main()
