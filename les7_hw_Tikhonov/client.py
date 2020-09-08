# скрипт моего клиента

from socket import *
import json
import sys
import time
from common.utils import msg_recv_func, msg_send_func
from common.variables import JIM_KEY_ACTION, JIM_KEY_TIME, JIM_KEY_USER, JIM_KEY_USER_ACCOUNT_NAME, \
    JIM_VALUE_PRESENCE, JIM_KEY_RESPONSE, JIM_KEY_ERROR, my_address, my_port, JIM_KEY_MESSAGE, \
    JIM_VALUE_MESSAGE, JIM_KEY_SENDER, my_client_mode
import logging
import logs.configs.config_client_log
from log_decorator import LogDeco
import argparse

# Включим логирование клиента
client_logger = logging.getLogger('client_logger')


#@LogDeco()
def arg_parser_func():
    parser_obj = argparse.ArgumentParser()
    parser_obj.add_argument('addr', default=my_address, nargs='?')
    parser_obj.add_argument('port', default=my_port, type=int, nargs='?')
    parser_obj.add_argument('-m', '--mode', default=my_client_mode, nargs='?')
    parsed_args = parser_obj.parse_args(sys.argv[1:])
    server_port = parsed_args.port
    server_addr = parsed_args.addr
    client_mode = parsed_args.mode

    if server_port < 1024 or server_port > 65535:
        client_logger.critical(f'Было введено некорретное значение порта.\n'
                               f'В качестве номера порта следует указать число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    if client_mode not in ('listen', 'send'):
        client_logger.critical(f'Указан неизвестный режим работы клиента.\n'
                               f'Ожидалось \'listen\' или \'send\'')
        sys.exit(1)

    return server_port, server_addr, client_mode


#@LogDeco()
def client_msg_presence_func(acc_name='Guest'):
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
    client_logger.debug('Сообщение для сервера сформировано.')
    return msg


#@LogDeco()
def client_msg_text_func(server_sock, acc_name='Guest'):
    """
    Функция формирует сообщение клиента для сервера
    :return:
    # {'action': 'message', 'time': 1573760672.167031, 'sender': 'Guest', 'message': 'Привет!'}
    """
    msg_text = input(f'Введите текст сообщения или \'!!!\' для завершения сеанса:\n')
    if msg_text == '!!!':
        print(f'Вы ввели {msg_text}. Сеанс соединения завершен.')
        server_sock.close()
        client_logger.info('Клиент решил завершить сеанс соединения с сервером.\n'
                           'Завершаем...')
        sys.exit(0)
    msg = {
        JIM_KEY_ACTION: JIM_VALUE_MESSAGE,
        JIM_KEY_TIME: time.time(),
        JIM_KEY_SENDER: acc_name,
        JIM_KEY_MESSAGE: msg_text
    }
    client_logger.debug('Сообщение для сервера сформировано.')
    return msg


#@LogDeco()
def ans_rework_func(server_ans):
    """
    Функция принимает декодированное сообщение от сервера, анализирует его
    и возвращает интерпретацию ответа сервера, взависимости от полученного
    кода ответа
    :param server_ans:
    # {"response": <код ответа>}
    :return:
    """
    client_logger.debug('Запуск функции интерпретирования ответа сервера...')
    if JIM_KEY_RESPONSE in server_ans:
        if server_ans[JIM_KEY_RESPONSE] == 200:
            client_logger.debug('Ответ сервера корректен. '
                                'Формируем штатную интерпретацию...')
            return 'Код ответа сервера: 200 ->> все хорошо.'
        else:
            client_logger.debug('Ответ сервера корректен, но присутствует код ошибки. '
                                'Формируем штатную интерпретацию...')
            return f'Код ответа сервера: 400.\n' \
                   f'Тект ошибки: {server_ans[JIM_KEY_ERROR]}'
    elif JIM_KEY_ACTION in server_ans and server_ans[JIM_KEY_ACTION] == JIM_VALUE_MESSAGE and \
            JIM_KEY_SENDER in server_ans and JIM_KEY_MESSAGE in server_ans:
        return f'Получено сообщение от {server_ans[JIM_KEY_SENDER]}:\n' \
               f'{server_ans[JIM_KEY_MESSAGE]}'
    else:
        client_logger.error('Ответ сервера некорректен. Поднимаем исключение...')
        raise ValueError


def main():
    """
    Запуск скрипта с параметрами
    # client.py 192.168.0.107 8888
    :return: 
    """
    client_logger.info('Запускаем работу клиента...')
    server_port, server_addr, client_mode = arg_parser_func()
    client_logger.info(f'Режим работы клиента: {client_mode}')

    try:
        server_sock = socket(AF_INET, SOCK_STREAM)
        server_sock.connect((server_addr, server_port))
        client_logger.info(f'Попытка подключения к серверу:\n'
                           f'Порт сервера: {server_port}\n'
                           f'Адрес сервера: {server_addr}')

        client_logger.info('Установлено соединение с сервером.')
        client_logger.debug('Формируем приветственное сообщение для сервера...')
        client_msg = client_msg_presence_func()
        client_logger.debug('Отправляем сообщение для сервера...')
        msg_send_func(client_msg, server_sock)

        client_logger.info('Ждем ответ от сервера...')
        server_ans = msg_recv_func(server_sock)
        client_logger.info('Получен ответ сервера...')
        client_logger.debug('Интерпретируем ответ сервера...')
        server_ans_reworked = ans_rework_func(server_ans)
        client_logger.info(f'Ответ сервера:\n'
                           f'{server_ans_reworked}')
    except ConnectionRefusedError as e:
        client_logger.critical('Ошибка: возможно скрипты клиента и сервара '
                               'были запущены с разными входными параметрами.'
                               'Или же сервер не запущен.')
        sys.exit(1)
    except (ValueError, json.JSONDecodeError) as e:
        client_logger.error(f'Принятое сообщение не содержит JSON-объект.')
        sys.exit(1)
    else:
        # Реализация режимов работы клиента
        while True:
            if client_mode == 'listen':
                try:
                    server_ans = msg_recv_func(server_sock)
                    server_ans_reworked = ans_rework_func(server_ans)
                    print(server_ans_reworked)
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError) as e:
                    client_logger.error(f'Соединение с сервером было потеряно.\n'
                                        f'Адрес сервера: {server_addr} ')
                    sys.exit(1)
            else:
                try:
                    client_msg_text = client_msg_text_func(server_sock)
                    msg_send_func(client_msg_text, server_sock)
                    client_logger.debug('Сообщение отправлено.')
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError) as e:
                    client_logger.error(f'Соединение с сервером было потеряно.\n'
                                        f'Адрес сервера: {server_addr} ')
                    sys.exit(1)


if __name__ == '__main__':
    main()

