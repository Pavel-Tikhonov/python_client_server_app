"""Мой декоратор для логирования"""

import sys
import logging
import logs.configs.config_sever_log
import logs.configs.config_client_log
import inspect
import traceback

# Определим, какой логгер нам следует запускать,
# в зависимости от того, откуда идет запрос на логирование:
if sys.argv[0].find('server') != -1:
    my_logger = logging.getLogger('server_logger')
else:
    my_logger = logging.getLogger('client_logger')

# Реализуем декоратор-логгер в виде класса:


class LogDeco:
    def __call__(self, func):
        def decorated(*args, **kwargs):
            func_result = func(*args, **kwargs)
            my_logger.debug(f'\nИдет вызов функции.\n'
                            f'Имя: {func.__name__}\n'
                            f'Позиционные аргументы: {args}\n'
                            f'Именованные аргументы: {kwargs}\n'
                            f'Функция-родитель: {inspect.stack()[1][3]}\n')
            return func_result
        return decorated

