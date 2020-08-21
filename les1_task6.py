"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.
"""
my_string = ['сетевое программирование', 'сокет', 'декоратор']
with open('test_file.txt', 'w') as f:
    f.writelines("\n".join(my_string))

print(f'Кодировка файла по умолчанию: {f.encoding}')

print('Содержимое файла в формате Unicode: ')
try:
    with open('test_file.txt', 'r', encoding='utf-8') as f:
        for line in f:
                print(line)
except UnicodeDecodeError as e:
    print('При чтении файла возникает ошибка, т.к. строки были записаны '
          'в файл в кодировке по умолчанию - cp1251,\n а прочитать содержимое мы хотим в кодировке utf-8.\n')


#Для успешного чтения содержимовго в utf-8 необходимо следующее:
with open('test_file.txt', 'rb') as f:
    for line in f:
        print(line.decode('cp1251').encode('utf-8').decode('utf-8'))






