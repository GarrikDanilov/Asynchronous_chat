import sys
import argparse
import socket
import select
import time
import common
import logging
import log.server_log_config
from decos import Log


class NotFoundError(Exception):
    pass


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


def process_msg(msg, logins, socks):
    if msg['to'] in logins and logins[msg['to']] in socks:
        common.send_msg(msg, logins[msg['to']])
        logger.info(f'Отправлено сообщение клиенту {msg["to"]} от {msg["from"]}')
    elif msg['to'] in logins and logins[msg['to']] not in socks:
        raise ConnectionError
    else:
        raise NotFoundError


def main(addr, port):
    sock = new_listen_socket(addr, port)

    clients = []
    logins = dict()
    r_clients = []
    w_clients = []
    err_list = []
    messages = []

    while True:
        try:
            client, client_addr = sock.accept()
        except OSError:
            pass
        else:
            logger.info(f'Установлено соединение с клиентом {client_addr}')
            clients.append(client)
        
        try:
            if clients:
                r_clients, w_clients, err_list = select.select(clients, clients, [])
        except OSError:
            pass

        if r_clients:
            for client in r_clients:
                try:
                    msg_from_client = common.get_msg(client)
                    if msg_from_client['action'] == 'presence':
                        msg_to_client = create_response(msg_from_client)
                        common.send_msg(msg_to_client, client)
                        logins[msg_from_client['user']['account_name']] = client
                    elif msg_from_client['action'] == 'msg':
                        messages.append(msg_from_client)
                except:
                    logger.info(f'Клиент {client.getpeername()} отключился от сервера')
                    clients.remove(client)

        for msg in messages:
            try:
                process_msg(msg, logins, w_clients)
            except ConnectionError:
                logger.info(f'Клиент {msg["to"]} отключился от сервера')
                clients.remove(logins[msg["to"]])
                del logins[msg["to"]]
            except NotFoundError:
                err_msg = {
                    'response': 404,
                    'error': f'Клиент {msg["to"]} отсутствует на сервере'
                }
                logger.error(f'Клиент {msg["to"]} отсутствует на сервере')
                try:
                    common.send_msg(err_msg, logins[msg['from']])
                except:
                    logger.info(f'Клиент {msg["from"]} отключился от сервера')
                    clients.remove(logins[msg["from"]])
                    del logins[msg["from"]]
        messages.clear()


if __name__ == '__main__':
    addr, port = get_args()
    main(addr, port)
