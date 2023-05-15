import os
import sys
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from client import create_presence


class TestClient(unittest.TestCase):
    test_msg = {
        'action': 'presence',
        'time': 1,
        'type': 'status',
        'user': {
            'account_name': 'test_account',
            'status': 'test'
        }
    }

    def test_create_presence(self):
        msg = create_presence('test_account', 'test')
        msg['time'] = 1
        self.assertEqual(msg, self.test_msg)


if __name__ == '__main__':
    unittest.main()
