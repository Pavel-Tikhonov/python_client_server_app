
from common.variables import JIM_KEY_RESPONSE, JIM_KEY_ERROR
import unittest
from ..server import server_ans_func


class TestServer(unittest.TestCase):
    """
    Тест функции server_ans_func()
    """
    ok_return = {JIM_KEY_RESPONSE: 200}
    er_return = {
            JIM_KEY_RESPONSE: 400,
            JIM_KEY_ERROR: 'JIM-protocol rules are not followed or incorrect user_name.'
        }

    def test_no_action_key(self):
        self.assertEqual(
            server_ans_func({'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}),
            self.er_return)

    def test_wrong_action_value(self):
        self.assertEqual(
            server_ans_func({'action': 'wrong presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}),
            self.er_return)

    def test_no_time_key(self):
        self.assertEqual(
            server_ans_func({'action': 'presence', 'user': {'account_name': 'Guest'}}),
            self.er_return)

    def test_no_user_key(self):
        self.assertEqual(
            server_ans_func({'action': 'presence',  'time': 1573760672.167031}),
            self.er_return)

    def test_wrong_acc_name(self):
        self.assertEqual(
            server_ans_func({'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'wrong Guest'}}),
            self.er_return)

    def test_ok_response(self):
        self.assertEqual(
            server_ans_func({'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}),
            self.ok_return)


if __name__ == '__main__':
    unittest.main()
