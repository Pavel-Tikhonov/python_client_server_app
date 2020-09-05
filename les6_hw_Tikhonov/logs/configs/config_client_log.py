"""Конфигурация моего клиентского логгера"""

import logging
import logging.handlers
import os
import sys
from common.variables import my_log_level

# Создание формировщика
# Сообщения лога должны иметь следующий формат: "<дата-время> <уровеньважности> <имямодуля> <сообщение>";
client_formatter_obj = logging.Formatter('%(asctime)s    %(levelname)-10s %(module)s %(message)s')

# Подготовим имя для файла логов
# вернем абсолютный путь до пакета configs
log_path = os.path.dirname(os.path.abspath(__file__))
# поднимемся на ур. выше и будем создавать логи там
log_path = os.path.join(log_path, '..', 'client.log')

# Создадим обработчики и настроим их
# Поток в командую строку
client_stream_handler = logging.StreamHandler(sys.stderr)
client_stream_handler.setFormatter(client_formatter_obj)
client_stream_handler.setLevel(my_log_level)
# Поток в файл
client_file_handler = logging.handlers.TimedRotatingFileHandler(
    log_path,
    encoding='utf-8',
    interval=1,
    when='D'
)
client_file_handler.setFormatter(client_formatter_obj)
client_file_handler.setLevel(my_log_level)

# Создадим регистратор верхнего уровня и настроим его
client_logger = logging.getLogger('client_logger')
client_logger.addHandler(client_stream_handler)
client_logger.addHandler(client_file_handler)
client_logger.setLevel(my_log_level)

# Проверим работу клиентского логгера
if __name__ == '__main__':
    client_logger.critical('Тест журнала критических ошибок')
    client_logger.error('Тест журнала обычных ошибок ошибок')
    client_logger.debug('Тест журнала отладки')
    client_logger.info('Тест журнала уведомлений')
