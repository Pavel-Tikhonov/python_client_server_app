"""
2. Задание на закрепление знаний по модулю json. Есть файл orders
в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий
его заполнение данными.

Для этого:
Создать функцию write_order_to_json(), в которую передается
5 параметров — товар (item), количество (quantity), цена (price),
покупатель (buyer), дата (date). Функция должна предусматривать запись
данных в виде словаря в файл orders.json. При записи данных указать
величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json()
с передачей в нее значений каждого параметра.

ПРОШУ ВАС НЕ УДАЛЯТЬ ИСХОДНЫЙ JSON-ФАЙЛ
ПРИМЕР ТОГО, ЧТО ДОЛЖНО ПОЛУЧИТЬСЯ

{
    "orders": [
        {
            "item": "printer",
            "quantity": "10",
            "price": "6700",
            "buyer": "Ivanov I.I.",
            "date": "24.09.2017"
        },
        {
            "item": "scaner",
            "quantity": "20",
            "price": "10000",
            "buyer": "Petrov P.P.",
            "date": "11.01.2018"
        }
    ]
}

вам нужно подгрузить JSON-объект
и достучаться до списка, который и нужно пополнять
а потом сохранять все в файл
"""
import json


def write_order_to_json(file_name, item, quantity, price, buyer, date):

    order_dict = {"item": item,
                  "quantity": quantity,
                  "price": price,
                  "buyer": buyer,
                  "date": date
                  }

    with open(file_name) as f_json:
        objs = json.load(f_json)

    for itm in objs.values():
        itm.append(order_dict)

    with open(file_name, 'w') as f_json:
        json.dump(objs, f_json, sort_keys=True, indent=4, ensure_ascii=False)


order_file_name = 'orders.json'
write_order_to_json(order_file_name, "Принтер", "10", "1500", "Иванов И.И.", "21.08.2020")
write_order_to_json(order_file_name, "Сканер", "15", "2300", "Петров П.П.", "22.08.2020")

with open(order_file_name) as f_n:
    print(f_n.read())



