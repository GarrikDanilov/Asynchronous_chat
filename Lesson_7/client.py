import sys
import argparse
import socket
import time
import logging
import common
import log.client_log_config
from decos import log


logger = logging.getLogger('client')


@log(logger)
def create_presence(account_name, status):
    msg = {
        'action': 'presence',
        'time': time.time(),
        'type': 'status',
        'user': {
            'account_name': account_name,
            'status': status
        }
    }

    logger.debug(f'Создано presence сообщение для пользователя {account_name}')

    return msg


def create_msg(addressee, account_name, msg):
    out = {
        'action': 'msg',
        'time': time.time(),
        'to': addressee,
        'from': account_name,
        'message': msg
    }

    logger.debug(f'Создано сообщение {out}')
    return out


def get_args():
    parser = argparse.ArgumentParser(description='Client script')
    parser.add_argument('addr', help='IP-адрес сервера')
    parser.add_argument('port', nargs='?', default=common.DEFAULT_PORT, type=int, 
                        help=f'TCP-порт на сервере, по умолчанию {common.DEFAULT_PORT}')
    
    args = parser.parse_args()
    if args.port < 1024 or args.port > 65535:
        logger.error(f'Некорректный номер порта - {args.port}. Номер порта должен быть \
в диапазоне от 1024 до 65535')
        sys.exit(1)     

    return args.addr, args.port 


def main(addr, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((addr, port))

    msg_to_server = create_presence('user1', 'active')
    common.send_msg(msg_to_server, sock)
    msg_from_server = common.get_msg(sock)
    logger.info(msg_from_server)
    sock.close()


if __name__ == '__main__':
    try:
        addr, port = get_args()
        main(addr, port)
    except ConnectionRefusedError:
        logger.critical(f'Не удалось подключиться к серверу - {addr}:{port}')


"""
2023-04-30 10:41:38,235 DEBUG decos Вызвана функция create_presence с аргументами ('user1', 'active'), {}.
  Вызов из модуля client.
  Функция create_presence вызвана из функции main.
"""
