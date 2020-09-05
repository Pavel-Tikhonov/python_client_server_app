# скрипт моего сервера
from socket import *
import sys
import json
from common.variables import my_address, my_port, my_max_connections, JIM_KEY_ACTION, \
    JIM_VALUE_PRESENCE, JIM_KEY_TIME, JIM_KEY_USER, JIM_KEY_USER_ACCOUNT_NAME, \
    JIM_KEY_RESPONSE, JIM_KEY_ERROR
from common.utils import msg_recv_func, msg_send_func
import logging
import logs.configs.config_sever_log
from log_decorator import LogDeco

# Включим логирование сервера
serv_logger = logging.getLogger('server_logger')


@LogDeco()
def server_ans_func(msg_obj):
    """
    Функция принимает объект декодированного сообщения(словарь), проверяет его
    на соответствие JIM-протоколу и формирует ответ сервера в виде словаря
    :param msg_obj:
    # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
    :return: server_ans
    """
    serv_logger.debug('Запуск функции формирования ответа сервера...')
    if JIM_KEY_ACTION in msg_obj and msg_obj[JIM_KEY_ACTION] == JIM_VALUE_PRESENCE and \
        JIM_KEY_TIME in msg_obj and JIM_KEY_USER in msg_obj and \
            msg_obj[JIM_KEY_USER][JIM_KEY_USER_ACCOUNT_NAME] == 'Guest':
        serv_logger.debug('Сообщение клиента соответствует JIM-протоколу. Формируем положительный ответ.')
        return {JIM_KEY_RESPONSE: 200}
    else:
        serv_logger.debug('Сообщение клиента не соответствует JIM-протоколу. Формируем отрицательный ответ.')
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
    serv_logger.info('Запуск сервера...')
    try:
        serv_logger.debug('Проверка входных параметров: порт...')
        if '-p' in sys.argv:
            server_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            server_port = my_port
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except ValueError as e:
        serv_logger.critical(f'Было введено некорретное значение порта.\n'
                             f'В качестве номера порта следует указать число в диапазоне от 1024 до 65535.')
        sys.exit(1)
    except IndexError as e:
        serv_logger.critical(f'Некорректный ввод входных параметров.\n'
                             f'После параметра "-p" не был указан номер порта.')
        sys.exit(1)
    serv_logger.debug('Проверка порта прошла успешно')

    try:
        serv_logger.debug('Проверка входных параметров: хост...')
        if '-a' in sys.argv:
            server_addr = sys.argv[sys.argv.index('-a') + 1]
        else:
            server_addr = my_address
    except IndexError as e:
        serv_logger.critical(f'Некорректный ввод входных параметров.\n'
                             f'После параметра "-a" не был указан адрес сервера.')
        sys.exit(1)
    serv_logger.debug('Проверка хоста прошла успешно')

    server_sock = socket(AF_INET, SOCK_STREAM)
    server_sock.bind((server_addr, server_port))
    server_sock.listen(my_max_connections)
    serv_logger.info(f'Сервер запущен и готов принимать запрос клиента.\n'
                     f'Порт сервера: {server_port}\n'
                     f'Адрес сервера: {server_addr}')

    while True:
        client_sock, client_addr = server_sock.accept()
        serv_logger.debug('Установлено соединение с клиентом...')
        try:
            client_msg = msg_recv_func(client_sock)
            serv_logger.debug(f'Получено сообщение:\n{client_msg}')
            server_ans = server_ans_func(client_msg)
            serv_logger.debug(f'Сформирован ответ сервера:\n{server_ans}')
            msg_send_func(server_ans, client_sock)
            serv_logger.debug(f'Ответ выслан клиенту.')
            client_sock.close()
            serv_logger.debug(f'Соединение с клиентом закрыто.')
        except (ValueError, json.JSONDecodeError) as e:
            serv_logger.error(f'Принятое сообщение не содержит JSON-объект.')
            client_sock.close()
            serv_logger.debug(f'Соединение с клиентом закрыто.')


if __name__ == '__main__':
    main()
