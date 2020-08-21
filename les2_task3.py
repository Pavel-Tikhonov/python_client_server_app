"""
3. Задание на закрепление знаний по модулю yaml.
 Написать скрипт, автоматизирующий сохранение данных
 в файле YAML-формата.
Для этого:

Подготовить данные для записи в виде словаря, в котором
первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа —
это целое число с юникод-символом, отсутствующим в кодировке
ASCII(например, €);

Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml. При этом обеспечить стилизацию файла с помощью
параметра default_flow_style, а также установить возможность работы
с юникодом: allow_unicode = True;

Реализовать считывание данных из созданного файла и проверить,
совпадают ли они с исходными.
"""
import yaml

names_list = ['Ivanov',
              'Sidorov',
              'Petrov']
ppl_total = 3
sl_dict = {"junior": "130€",
           "middle": "300€",
           "senior": "450€"}

data_to_yaml = {"names": names_list,
                "quantity": ppl_total,
                "salary": sl_dict}

with open('my_file.yaml', 'w') as f_ya:
    yaml.dump(data_to_yaml, f_ya, default_flow_style=False, allow_unicode=True)

with open('my_file.yaml') as f_ya:
    print(f_ya.read())
