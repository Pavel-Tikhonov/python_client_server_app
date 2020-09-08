# скрипт моего сервера
from socket import *
import sys
import json
from common.variables import my_address, my_port, my_max_connections, JIM_KEY_ACTION, \
    JIM_VALUE_PRESENCE, JIM_KEY_TIME, JIM_KEY_USER, JIM_KEY_USER_ACCOUNT_NAME, \
    JIM_KEY_RESPONSE, JIM_KEY_ERROR, JIM_KEY_MESSAGE, JIM_VALUE_MESSAGE, JIM_KEY_SENDER
from common.utils import msg_recv_func, msg_send_func
import logging
import logs.configs.config_sever_log
from log_decorator import LogDeco
import select
import argparse
import time

# Включим логирование сервера
serv_logger = logging.getLogger('server_logger')


#@LogDeco()
def arg_parser_func():
    parser_obj = argparse.ArgumentParser()
    parser_obj.add_argument('-p', default=my_port, type=int, nargs='?')
    parser_obj.add_argument('-a', default=my_address, nargs='?')
    parsed_args = parser_obj.parse_args(sys.argv[1:])
    server_port = parsed_args.p
    server_addr = parsed_args.a

    if server_port < 1024 or server_port > 65535:
        serv_logger.critical(f'Было введено некорретное значение порта.\n'
                             f'В качестве номера порта следует указать число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    return server_port, server_addr


#@LogDeco()
def server_ans_func(msg_obj, all_messages, client_sock):
    """
    :param msg_obj:
    # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
    # {'action': 'message', 'time': 1573760672.167031, 'sender': 'Guest', 'message': 'Привет!'}
    :param all_messages:
    :param client_sock:
    :return:
    """
    # Проверка приветственного сообщения
    if JIM_KEY_ACTION in msg_obj and msg_obj[JIM_KEY_ACTION] == JIM_VALUE_PRESENCE and \
        JIM_KEY_TIME in msg_obj and JIM_KEY_USER in msg_obj and \
            msg_obj[JIM_KEY_USER][JIM_KEY_USER_ACCOUNT_NAME] == 'Guest':
        serv_logger.debug('Приняли приветственное сообщение клиента. Формируем положительный ответ.')
        server_ans = {JIM_KEY_RESPONSE: 200}
        msg_send_func(server_ans, client_sock)
        return
    # Проверка текстового сообщения для чата
    elif JIM_KEY_ACTION in msg_obj and msg_obj[JIM_KEY_ACTION] == JIM_VALUE_MESSAGE and \
            JIM_KEY_TIME in msg_obj and JIM_KEY_MESSAGE in msg_obj and JIM_KEY_SENDER in msg_obj:
        all_messages.append((msg_obj[JIM_KEY_SENDER], msg_obj[JIM_KEY_MESSAGE]))
        return
    else:
        serv_logger.debug('Сообщение клиента не соответствует JIM-протоколу. Формируем отрицательный ответ.')
        server_ans = {
            JIM_KEY_RESPONSE: 400,
            JIM_KEY_ERROR: 'JIM-protocol rules are not followed or incorrect user_name.'
        }
        msg_send_func(server_ans, client_sock)
        return


def main():
    '''
    Вызов скрипта с параметрами
    server.py -p 8888 -a 192.168.0.107
    :return:
    '''
    serv_logger.info('Запуск сервера...')
    serv_logger.debug('Парсинг входных параметров...')
    server_port, server_addr = arg_parser_func()
    serv_logger.debug('Парсинг входных параметров завершен.')

    server_sock = socket(AF_INET, SOCK_STREAM)
    server_sock.bind((server_addr, server_port))
    server_sock.settimeout(0.2)
    server_sock.listen(my_max_connections)
    serv_logger.info(f'Сервер запущен и готов принимать запрос клиента.\n'
                     f'Порт сервера: {server_port}\n'
                     f'Адрес сервера: {server_addr}')

    all_clients = []
    all_messages = []

    while True:
        try:
            client_sock, client_addr = server_sock.accept()
        except OSError as e:
            pass
        else:
            serv_logger.debug(f'Установлено соединение с клиентом:\n '
                              f'Адресс клиента: {client_addr}')
            all_clients.append(client_sock)

        # Готовимся к работе с select
        clients_to_read = []
        clients_to_write = []
        # clients_with_errors = []

        try:
            clients_to_read, clients_to_write, clients_with_errors = \
                select.select(all_clients, all_clients, [], 0)
        except OSError as e:
            pass

        # Работа с клиентами, у которых есть для нас сообщение
        if clients_to_read:
            serv_logger.debug('Обнаружены клиенты с сообщениями. Читаем...')
            for client_sock in clients_to_read:
                try:
                    server_ans_func(msg_recv_func(client_sock), all_messages, client_sock)
                    serv_logger.debug('Сообщение клиента обработано, добавлено в список сообщений.')
                except Exception as e:
                    serv_logger.info(f'Клиент отключился от сервера.\n'
                                     f'Информауция о клиенте:\n'
                                     f'{client_sock.getpeername()}')
                    all_clients.remove(client_sock)

        # Работа с текстовыми сообщениями для чата
        if all_messages and clients_to_write:
            serv_logger.debug('У нас есть сообщения для отправки, а также клиенты, ожидающие сообщения.')
            serv_logger.debug('Формируем сообщение для очередного клиента.')
            server_ans = {
                JIM_KEY_ACTION: JIM_VALUE_MESSAGE,
                JIM_KEY_TIME: time.time(),
                JIM_KEY_SENDER: all_messages[0][0],
                JIM_KEY_MESSAGE: all_messages[0][1]
            }
            del all_messages[0]
            # Отправка ответов ожидающим клиентам
            for client_sock in clients_to_write:
                try:
                    serv_logger.debug('Отправляем сообщение для клиента.')
                    msg_send_func(server_ans, client_sock)
                    serv_logger.debug('Сообщение отправлено.\n'
                                      f'{server_ans}')
                except Exception as e:
                    serv_logger.info(f'Клиент отключился от сервера.\n'
                                     f'Информауция о клиенте:\n'
                                     f'{client_sock.getpeername()}')
                    all_clients.remove(client_sock)


if __name__ == '__main__':
    main()
