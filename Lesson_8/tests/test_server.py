import os
import sys
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from server import create_response


class TestServer(unittest.TestCase):
    res_200 = {
        'response': 200,
            'time': 1,
            'alert': '200, OK'
    }
    res_400 = {
        'response': 400,
        'time': 1,
        'error': '400, Bad request'
    }

    def test_create_response_200(self):
        msg = {'action': 'presence'}
        res = create_response(msg)
        res['time'] = 1
        self.assertEqual(res, self.res_200)

    def test_create_response(self):
        msg = {'action': 'msg'}
        res = create_response(msg)
        res['time'] = 1
        self.assertEqual(res, self.res_400)


if __name__ == '__main__':
    unittest.main()
