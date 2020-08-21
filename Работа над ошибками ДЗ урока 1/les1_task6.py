"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.
"""
my_string = ['сетевое программирование', 'сокет', 'декоратор']
with open('test_file.txt', 'w') as f:
    f.writelines("\n".join(my_string))

print(f'Кодировка файла по умолчанию: {f.encoding}')

print('Содержимое файла в формате Unicode: ')

# Для успешного чтения содержимовго в utf-8 необходимо следующее:
with open('test_file.txt', 'rb') as f:
    for line in f:
        print(line.decode('cp1251').encode('utf-8').decode('utf-8'))






