import sys
import socket
import common
from client import logger, create_presence, get_args, create_msg


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
        msg = input('Введите сообщение для отправки: ')
        common.send_msg(create_msg('#all', 'client', msg), sock)


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
    