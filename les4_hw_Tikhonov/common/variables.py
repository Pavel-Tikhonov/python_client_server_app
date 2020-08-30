# Мои константы

# Входные данные для запуска сервера
my_address = '127.0.0.1'
my_port = 7777
my_max_connections = 5

# Данные для обработки сообщения
my_max_package = 1024
my_encoding = 'utf-8'

# Ключи JIM-протокола
"""
Пример сообщения со стороны клиента
{
        "action": "presence",
        "time": <unix timestamp>,
        "type": "status",
        "user": {
                "account_name":  "C0deMaver1ck",
        }
}

Пример ответа сервера
{
    "response": 200,
    "alert"/"error":"Необязательное сообщение/уведомление"
}
"""
JIM_KEY_ACTION = 'action'
JIM_KEY_TIME = 'time'
JIM_KEY_TYPE = 'type'
JIM_KEY_USER = 'user'
JIM_KEY_USER_ACCOUNT_NAME = 'account_name'
JIM_KEY_ERROR = 'error'
JIM_KEY_RESPONSE = 'response'
JIM_VALUE_PRESENCE = 'presence'
JIM_VALUE_STATUS = 'status'


