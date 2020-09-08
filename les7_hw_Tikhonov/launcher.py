# скрипт моего лаунчера
import subprocess

my_process = []

while True:
    todo = input('Выберите действие:\n'
                 'q - выход\n'
                 's - запуск скриптов сервера и клиентов: 2 на send, 2 на listen\n'
                 'x - остановка сервера\n')

    if todo == 'q':
        print('Выход из лаунчера.')
        break
    elif todo == 's':
        my_process.append(subprocess.Popen('python server.py -p 8888 -a 192.168.0.107',
                                           creationflags=subprocess.CREATE_NEW_CONSOLE))
        for _ in range(2):
            my_process.append(subprocess.Popen('python client.py 192.168.0.107 8888 -m send',
                                               creationflags=subprocess.CREATE_NEW_CONSOLE))
        for _ in range(2):
            my_process.append(subprocess.Popen('python client.py 192.168.0.107 8888 -m listen',
                                               creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif todo == 'x':
        while my_process:
            VICTIM = my_process.pop()
            print(f'Остановка процесса {VICTIM}...')
            VICTIM.kill()
        print('Запущенные процессы из списка my_process были остановлены, если они там были.')
    else:
        print('Была введена некорректная команда.')
