"""Конфигурация моего серверного логгера"""

import logging
import logging.handlers
import os
import sys
from common.variables import my_log_level


# Создание формировщика
# Сообщения лога должны иметь следующий формат: "<дата-время> <уровеньважности> <имямодуля> <сообщение>";
serv_formatter_obj = logging.Formatter('%(asctime)s    %(levelname)-10s %(module)s %(message)s')

# Подготовим имя для файла логов
# вернем абсолютный путь до пакета configs
log_path = os.path.dirname(os.path.abspath(__file__))
# поднимемся на ур. выше и будем создавать логи там
log_path = os.path.join(log_path, '..', 'server.log')

# Создадим обработчики и настроим их
# Поток в командую строку
serv_stream_handler = logging.StreamHandler(sys.stderr)
serv_stream_handler.setFormatter(serv_formatter_obj)
serv_stream_handler.setLevel(my_log_level)
# Поток в файл
serv_file_handler = logging.handlers.TimedRotatingFileHandler(
    log_path,
    encoding='utf-8',
    interval=1,
    when='D'
)
serv_file_handler.setFormatter(serv_formatter_obj)
serv_file_handler.setLevel(my_log_level)

# Создадим регистратор верхнего уровня и настроим его
serv_logger = logging.getLogger('server_logger')
serv_logger.addHandler(serv_stream_handler)
serv_logger.addHandler(serv_file_handler)
serv_logger.setLevel(my_log_level)

# Проверим работу серверного логгера
if __name__ == '__main__':
    serv_logger.critical('Тест журнала критических ошибок')
    serv_logger.error('Тест журнала обычных ошибок ошибок')
    serv_logger.debug('Тест журнала отладки')
    serv_logger.info('Тест журнала уведомлений')




