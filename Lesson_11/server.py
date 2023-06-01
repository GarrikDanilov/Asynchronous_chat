import argparse
import logging
import socket
import select
import time
from common import DEFAULT_PORT, MAX_CONNECTIONS, MAX_TIMEOUT, send_msg, get_msg
import log.server_log_config
from decos import Log
from descriptors import ValidatingPort
from metaclasses import ServerVerifier


logger = logging.getLogger('server')


class NotFoundError(Exception):
    pass


def get_args():
    parser = argparse.ArgumentParser(description='Server script')
    parser.add_argument('-p', dest='port', default=DEFAULT_PORT, type=int, 
                        help=f'TCP-порт, по умолчанию {DEFAULT_PORT}')
    parser.add_argument('-a', dest='addr', default='', 
                        help='IP-адрес для прослушивания, по умолчанию все доступные адреса')
    
    args = parser.parse_args()    

    return args.addr, args.port


class Server(metaclass=ServerVerifier):
    port = ValidatingPort(logger)

    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.clients = []
        self.logins = dict()
        self.messages = []
    
    def create_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.addr, self.port))
        self.sock.listen(MAX_CONNECTIONS)
        self.sock.settimeout(MAX_TIMEOUT)

    @Log(logger)
    def create_response(self, msg):
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
    
    def process_msg(self, msg, socks):
        if msg['to'] in self.logins and self.logins[msg['to']] in socks:
            send_msg(msg, self.logins[msg['to']])
            logger.info(f'Отправлено сообщение клиенту {msg["to"]} от {msg["from"]}')
        elif msg['to'] in self.logins and self.logins[msg['to']] not in socks:
            raise ConnectionError
        else:
            raise NotFoundError
    
    def main_loop(self):
        self.create_socket()

        r_clients = []
        w_clients = []
        err_list = []

        while True:
            try:
                client, client_addr = self.sock.accept()
            except OSError:
                pass
            else:
                logger.info(f'Установлено соединение с клиентом {client_addr}')
                self.clients.append(client)
        
            try:
                if self.clients:
                    r_clients, w_clients, err_list = select.select(self.clients, self.clients, [])
            except OSError:
                pass

            if r_clients:
                for client in r_clients:
                    try:
                        msg_from_client = get_msg(client)
                        if msg_from_client['action'] == 'presence':
                            msg_to_client = self.create_response(msg_from_client)
                            send_msg(msg_to_client, client)
                            self.logins[msg_from_client['user']['account_name']] = client
                        elif msg_from_client['action'] == 'msg':
                            self.messages.append(msg_from_client)
                    except:
                        logger.info(f'Клиент {client.getpeername()} отключился от сервера')
                        self.clients.remove(client)

            for msg in self.messages:
                try:
                    self.process_msg(msg, w_clients)
                except ConnectionError:
                    logger.info(f'Клиент {msg["to"]} отключился от сервера')
                    self.clients.remove(self.logins[msg["to"]])
                    del self.logins[msg["to"]]
                except NotFoundError:
                    err_msg = {
                        'response': 404,
                        'error': f'Клиент {msg["to"]} отсутствует на сервере'
                    }
                    logger.error(f'Клиент {msg["to"]} отсутствует на сервере')
                    try:
                        send_msg(err_msg, self.logins[msg['from']])
                    except:
                        logger.info(f'Клиент {msg["from"]} отключился от сервера')
                        self.clients.remove(self.logins[msg["from"]])
                        del self.logins[msg["from"]]
            self.messages.clear()


def main():
    addr, port = get_args()

    server = Server(addr, port)
    server.main_loop()


if __name__ == '__main__':
    main()
