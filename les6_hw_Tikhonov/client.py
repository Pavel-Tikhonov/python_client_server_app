# скрипт моего клиента

from socket import *
import json
import sys
import time
from common.utils import msg_recv_func, msg_send_func
from common.variables import JIM_KEY_ACTION, JIM_KEY_TIME, JIM_KEY_USER, JIM_KEY_USER_ACCOUNT_NAME, \
    JIM_VALUE_PRESENCE, JIM_KEY_RESPONSE, JIM_KEY_ERROR, my_address, my_port
import logging
import logs.configs.config_client_log
from log_decorator import LogDeco

# Включим логирование клиента
client_logger = logging.getLogger('client_logger')


@LogDeco()
def client_msg_func(acc_name='Guest'):
    """
    Функция формирует сообщение клиента для сервера
    :return:
    # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
    """
    client_logger.debug('Запуск функции формирования сообщения для сервера...')
    msg = {
        JIM_KEY_ACTION: JIM_VALUE_PRESENCE,
        JIM_KEY_TIME: time.time(),
        JIM_KEY_USER: {
            JIM_KEY_USER_ACCOUNT_NAME: acc_name
        }
    }
    client_logger.debug('Сообщение для сервера сформировано.')
    return msg


@LogDeco()
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
    try:
        client_logger.debug('Запускаем проверку входных данных: порт и хост...')
        server_addr = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError as e:
        server_addr = my_address
        server_port = my_port
    except ValueError as e:
        client_logger.critical('Некорректный номер порта. '
                               'В качестве номера порта следует указать число в диапазоне от 1024 до 65535.')
        sys.exit(1)
    client_logger.debug('Проверка входных данных прошла успешно.')

    server_sock = socket(AF_INET, SOCK_STREAM)
    client_logger.info(f'Попытка подключения к серверу:\n'
                       f'Порт сервера: {server_port}\n'
                       f'Адрес сервера: {server_addr}')
    try:
        server_sock.connect((server_addr, server_port))
    except ConnectionRefusedError as e:
        client_logger.critical('Ошибка: возможно скрипты клиента и сервара '
                               'были запущены с разными входными параметрами.'
                               'Или же сервер не запущен.')
        sys.exit(1)

    client_logger.debug('Формируем сообщение для сервера...')
    client_msg = client_msg_func()
    client_logger.debug('Отправляем сообщение для сервера...')
    msg_send_func(client_msg, server_sock)
    try:
        client_logger.debug('Получаем ответ сервера...')
        server_ans = msg_recv_func(server_sock)
        client_logger.debug('Интерпретируем ответ сервера...')
        server_ans_reworked = ans_rework_func(server_ans)
        server_sock.close()
        client_logger.debug('Закрываем соединение с сервером')
        print(server_ans_reworked)
        """
        input("Скрипт на паузе. Нажмите enter для продолжения.\n"
              "Я это сделал, чтобы при запуске этого скрипта через лаунчер его консоль не закрывалась сразу\n"
              "по завершению скрипта, тк у меня в нем нет конструкции while True...Я решил послать серверу запрос\n"
              "только 1 раз.")
        """
    except (ValueError, json.JSONDecodeError) as e:
        client_logger.error(f'Принятое сообщение не содержит JSON-объект.')
        print('Принятое сообщение не содержит JSON-объект.')
        server_sock.close()
        client_logger.debug('Закрываем соединение с сервером')


if __name__ == '__main__':
    main()

