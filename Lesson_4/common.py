import json


DEFAULT_PORT = 7777
MAX_CONNECTIONS = 5
MAX_MSG_SIZE = 1024
DEFAULT_ENCODING = 'utf-8'


def get_msg(sock):
    recv_msg = sock.recv(MAX_MSG_SIZE).decode(DEFAULT_ENCODING)
    return json.loads(recv_msg)


def send_msg(msg, sock):
    out = json.dumps(msg)
    sock.send(out.encode(DEFAULT_ENCODING))
