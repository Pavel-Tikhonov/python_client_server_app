"""
4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое
и выполнить обратное преобразование (используя методы encode и decode).
"""
my_list = ['разработка', 'protocol', 'standard', 'администрирование']
print(f'Массив my_list до преобразования: \n{my_list}')

my_list_bytes = list((itm.encode('utf-8') for itm in my_list))
print(f'\nМассив my_list после преобразования в байты:')
for itm in my_list_bytes:
    print(itm)

my_list_bytes_to_str = list((itm.decode('utf-8') for itm in my_list_bytes))
print(f'\nМассив my_list после обратного преобразования в строки: \n{my_list_bytes_to_str}')



