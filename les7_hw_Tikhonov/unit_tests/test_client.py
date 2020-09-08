from common.variables import JIM_KEY_ACTION, JIM_KEY_TIME, JIM_KEY_USER, JIM_KEY_USER_ACCOUNT_NAME, \
    JIM_VALUE_PRESENCE, JIM_KEY_RESPONSE, JIM_KEY_ERROR
import unittest
from client import client_msg_func, ans_rework_func


class TestClient(unittest.TestCase):
    """
    Тест функции client_msg_func()
    """
    client_msg_func_acc_name = "my own Guest"
    client_msg_func_ok_response = {
        JIM_KEY_ACTION: JIM_VALUE_PRESENCE,
        JIM_KEY_TIME: 1.1,
        JIM_KEY_USER: {
            JIM_KEY_USER_ACCOUNT_NAME: client_msg_func_acc_name
        }
    }

    client_msg_func_ok_response_default = {
        JIM_KEY_ACTION: JIM_VALUE_PRESENCE,
        JIM_KEY_TIME: 1.1,
        JIM_KEY_USER: {
            JIM_KEY_USER_ACCOUNT_NAME: 'Guest'
        }
    }

    def test_client_msg_func_ok_response(self):
        test_foo = client_msg_func(self.client_msg_func_acc_name)
        test_foo[JIM_KEY_TIME] = 1.1
        self.assertEqual(test_foo, self.client_msg_func_ok_response)

    def test_client_msg_func_ok_response_default(self):
        test_foo = client_msg_func()
        test_foo[JIM_KEY_TIME] = 1.1
        self.assertEqual(test_foo, self.client_msg_func_ok_response_default)

    """
    Тест функции ans_rework_func()
    """
    server_ok_ans = {JIM_KEY_RESPONSE: 200}
    server_er_ans = {
            JIM_KEY_RESPONSE: 400,
            JIM_KEY_ERROR: 'JIM-protocol rules are not followed or incorrect user_name.'
        }
    server_except_ans = {}
    ans_rework_func_ok_response = 'Код ответа сервера: 200 ->> все хорошо.'
    ans_rework_func_er_response = f'Код ответа сервера: 400.\n' \
                                  f'Тект ошибки: {server_er_ans[JIM_KEY_ERROR]}'

    def test_ans_rework_func_ok_response(self):
        self.assertEqual(ans_rework_func(self.server_ok_ans), self.ans_rework_func_ok_response)

    def test_ans_rework_func_er_response(self):
        self.assertEqual(ans_rework_func(self.server_er_ans), self.ans_rework_func_er_response)

    def test_ans_rework_func_no_response(self):
        with self.assertRaises(ValueError):
            ans_rework_func(self.server_except_ans)


if __name__ == '__main__':
    unittest.main()
