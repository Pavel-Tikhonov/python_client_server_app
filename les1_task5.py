"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового
в строковый тип на кириллице.
"""
import chardet
import subprocess

"""
Известно, что на вычислительных устройствах под управлением русифицированной ОС Windows при запуске
консольных приложений чаще всего используется кириллическая кодировка cp866.
Однако, используя chardet, было определено, что большинство строк был закодировано при кодировке IBM866.
Решил попробовать автоматизировать процесс определения наиболее часто встречающейся кодировки при обработке запроса.
"""

#args = ['ping', 'yandex.ru']


def my_ping(args):

    subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)

    print(f'Попытка применить модуль chardet к определению исходной кодировки входных данных ресурса {args[1]}: ')
    my_encoding = []
    for line in subproc_ping.stdout:
        result = chardet.detect(line)
        charenc = result['encoding']
        my_encoding.append(charenc)

    print(f'Встреченные при обработке запроса кодировки:\n{my_encoding}')
    my_encoding_unique = set(my_encoding)
    my_dict = {}
    for itm in my_encoding_unique:
        my_dict[itm] = my_encoding.count(itm)

    my_count_max = max(my_dict.values())
    my_dict_inv = {value: key for key, value in my_dict.items()}
    my_encoding_finish = my_dict_inv[my_count_max]
    print(f'Наиболее часто встречаемая в запросе кодировка с точки зрения chardet:\n {my_encoding_finish}')
    print(f'Используем кодировку {my_encoding_finish} для обработки дальнейших запросов')

    subproc_ping_check = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in subproc_ping_check.stdout:
        print(line.decode(my_encoding_finish).encode('utf-8').decode('utf-8'))


my_ping(['ping', 'yandex.ru'])
my_ping(['ping', 'youtube.com'])


