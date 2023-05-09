import sys
import socket
import common
from client import logger, create_presence, get_args


class ServerError(Exception):
    pass


def main(addr, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((addr, port))

    common.send_msg(create_presence('client', 'active'), sock)
    msg_from_server = common.get_msg(sock)
    if msg_from_server['response'] == 400:
        raise ServerError(msg_from_server['error'])
    logger.info('Соединение с сервером установлено')

    while True:
        msg_from_server = common.get_msg(sock)
        logger.info(f'Получено сообщение: {msg_from_server}')
        print(f'Получено сообщение: {msg_from_server}')


if __name__ == '__main__':
    try:
        addr, port = get_args()
        main(addr, port)
    except ConnectionRefusedError:
        logger.critical(f'Не удалось подключиться к серверу - {addr}:{port}')
        sys.exit(1)
    except ServerError as e:
        logger.error(f'При установке соединения сервер вернул ошибку - {e}')
        sys.exit(1)
        