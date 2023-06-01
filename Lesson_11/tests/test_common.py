import os
import sys
import json
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
import common


class TestSocket:
    def __init__(self, test_dict):
        self.test_msg = json.dumps(test_dict).encode(common.DEFAULT_ENCODING)
        self.recv_msg = None

    def send(self, msg):
        self.recv_msg = msg

    def recv(self, len):
        return self.test_msg


class TestCommon(unittest.TestCase):
    msg_send = {
        'action': 'presence',
        'time': 1,
        'type': 'status',
        'user': {
            'account_name': 'test_account',
            'status': 'test'
        }
    }
    msg_recv = {
        'response': 200,
            'time': 1,
            'alert': '200, OK'
    }

    def test_get_msg(self):
        test_sock = TestSocket(self.msg_recv)
        msg = common.get_msg(test_sock)
        self.assertEqual(msg, self.msg_recv)

    def test_send_msg(self):
        test_sock = TestSocket(self.msg_send)
        common.send_msg(self.msg_send, test_sock)
        self.assertEqual(test_sock.recv_msg, test_sock.test_msg)


if __name__ == '__main__':
    unittest.main()
