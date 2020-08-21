"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно
получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data
(также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

Пример того, что должно получиться:

Изготовитель системы,Название ОС,Код продукта,Тип системы

1,LENOVO,Windows 7,00971-OEM-1982661-00231,x64-based

2,ACER,Windows 10,00971-OEM-1982661-00231,x64-based

3,DELL,Windows 8.1,00971-OEM-1982661-00231,x86-based

Обязательно проверьте, что у вас получается примерно то же самое.

ПРОШУ ВАС НЕ УДАЛЯТЬ СЛУЖЕБНЫЕ ФАЙЛЫ TXT И ИТОГОВЫЙ ФАЙЛ CSV!!!
"""

import re
import csv


def get_data(names_list):

    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    for itm in names_list:
        with open(itm, 'r') as f:
            for line in f:
                if re.search(r'Изготовитель системы', line) is not None:
                    info = re.split(r'\s{2,}', line)
                    os_prod_list.append(re.search(r'.+', info[-1]).group(0))
                elif re.search(r'Название ОС', line) is not None:
                    info = re.split(r'\s{2,}', line)
                    os_name_list.append(re.search(r'.+', info[-1]).group(0))
                elif re.search(r'Код продукта', line) is not None:
                    info = re.split(r'\s{2,}', line)
                    os_code_list.append(re.search(r'.+', info[-1]).group(0))
                elif re.search(r'Тип системы', line) is not None:
                    info = re.split(r'\s{2,}', line)
                    os_type_list.append(re.search(r'.+', info[-1]).group(0))

    headers_list = ['Изготовитель систем', 'Название ОС', 'Код продукта', 'Тип системы']
    main_data = [headers_list]
    for i, _ in enumerate(range(3), 1):
        main_data.append([i, os_prod_list[i-1], os_name_list[i-1], os_code_list[i-1], os_type_list[i-1]])
    return main_data


def write_to_csv(data_list, file_name):
    data = get_data(data_list)
    with open(file_name, 'w') as f:
        f_writer = csv.writer(f)
        for row in data:
            f_writer.writerow(row)


my_list = ['info_1.txt', 'info_2.txt', 'info_3.txt']
my_file = 'les2_task1_result.csv'
write_to_csv(my_list, my_file)

with open(my_file) as f:
    print(f.read())





