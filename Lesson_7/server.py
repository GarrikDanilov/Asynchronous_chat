import sys
import argparse
import socket
import time
import common
import logging
import log.server_log_config
from decos import Log


logger = logging.getLogger('server')


@Log(logger)
def create_response(msg):
    if 'action' in msg and msg['action'] == 'presence':
        logger.debug('Создан ответ клиенту с кодом 200')
        return {
            'response': 200,
            'time':time.time(),
            'alert': '200, OK'
        }
    
    logger.debug('Создан ответ клиенту с кодом 400')
    return {
        'response': 400,
        'time':time.time(),
        'error': '400, Bad request'
    }


def get_args():
    parser = argparse.ArgumentParser(description='Server script')
    parser.add_argument('-p', dest='port', default=common.DEFAULT_PORT, type=int, 
                        help=f'TCP-порт, по умолчанию {common.DEFAULT_PORT}')
    parser.add_argument('-a', dest='addr', default='', 
                        help='IP-адрес для прослушивания, по умолчанию все доступные адреса')
    
    args = parser.parse_args()
    if args.port < 1024 or args.port > 65535:
        logger.error(f'Некорректный номер порта - {args.port}. Номер порта должен быть \
в диапазоне от 1024 до 65535')
        sys.exit(1)     

    return args.addr, args.port


def new_listen_socket(addr, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((addr, port))
    sock.listen(common.MAX_CONNECTIONS)
    sock.settimeout(common.MAX_TIMEOUT)

    return sock


def main(addr, port):
    sock = new_listen_socket(addr, port)

    while True:
        client, addr = sock.accept()
        msg_from_client = common.get_msg(client)
        logger.info(msg_from_client)
        msg_to_client = create_response(msg_from_client)
        common.send_msg(msg_to_client, client)
        client.close()


if __name__ == '__main__':
    addr, port = get_args()
    main(addr, port)


"""
2023-04-30 10:49:31,703 DEBUG decos Вызвана функция create_response с аргументами 
({'action': 'presence', 'time': 1682840971.70171, 'type': 'status', 'user': {'account_name': 'user1', 'status': 'active'}},), {}.
  Вызов из модуля server.
  Функция create_response вызвана из функции main.
"""
