import sys
import socket
import common
from client import logger, create_presence, get_args, create_msg, ServerError


def main(login, addr, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((addr, port))

    common.send_msg(create_presence(login, 'active'), sock)
    msg_from_server = common.get_msg(sock)
    if msg_from_server['response'] == 400:
        raise ServerError(msg_from_server['error'])
    logger.info('Соединение с сервером установлено')

    while True:
        to_client = input('Введите получателя: ')
        msg = input('Введите сообщение для отправки: ')
        common.send_msg(create_msg(to_client, login, msg), sock)


if __name__ == '__main__':
    try:
        login, addr, port = get_args()
        main(login, addr, port)
    except ConnectionRefusedError:
        logger.critical(f'Не удалось подключиться к серверу - {addr}:{port}')
        sys.exit(1)
    except ServerError as e:
        logger.error(f'При установке соединения сервер вернул ошибку - {e}')
        sys.exit(1)