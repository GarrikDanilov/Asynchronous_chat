import sys
import argparse
import socket
import time
import threading
import logging
import log.client_log_config
from common import DEFAULT_PORT, send_msg, get_msg
from decos import log
from metaclasses import ClientVerifier


class ServerError(Exception):
    pass


logger = logging.getLogger('client')


def get_args():
    parser = argparse.ArgumentParser(description='Client script')
    parser.add_argument('login', help='Логин')
    parser.add_argument('addr', help='IP-адрес сервера')
    parser.add_argument('port', nargs='?', default=DEFAULT_PORT, type=int, 
                        help=f'TCP-порт на сервере, по умолчанию {DEFAULT_PORT}')
    
    args = parser.parse_args()
    if args.port < 1024 or args.port > 65535:
        logger.error(f'Некорректный номер порта - {args.port}. Номер порта должен быть \
в диапазоне от 1024 до 65535')
        sys.exit(1)     

    return args.login, args.addr, args.port 


class Client(metaclass=ClientVerifier):

    def __init__(self, login, sock, status='active'):
        self.login = login
        self.sock = sock
        self.status = status

    @log(logger)
    def create_presence(self):
        msg = {
            'action': 'presence',
            'time': time.time(),
            'type': 'status',
            'user': {
                'account_name': self.login,
                'status': self.status
            }
        }

        logger.debug(f'Создано presence сообщение для пользователя {self.login}')

        return msg
    
    def create(self):
        send_msg(self.create_presence(), self.sock)
        msg_from_server = get_msg(self.sock)
        if msg_from_server['response'] == 400:
            raise ServerError(msg_from_server['error'])
        logger.info('Соединение с сервером установлено')
    
    def create_msg(self, addressee, msg):
        out = {
            'action': 'msg',
            'time': time.time(),
            'to': addressee,
            'from': self.login,
            'message': msg
        }

        logger.debug(f'Создано сообщение {out}')
        return out
    
    def to_server(self):
        while True:
            command = input('Отправить сообщение (s)/ Выйти (q): ')

            if command == 'q':
                self.sock.close()
                break
            elif command == 's':
                to_client = input('Введите получателя: ')
                message = input('Введите сообщение: ')

                try:
                    send_msg(self.create_msg(to_client, message), self.sock)
                except:
                    logger.critical(f'Соединение с сервером потеряно')
                    break

    def from_server(self):
        while True:
            try:
                message = get_msg(self.sock)
                if 'response' in message:
                    print(f'\nОшибка: {message["error"]}')
                else:
                    print(f'\n{message["from"]}: {message["message"]}')
            except:
                logger.critical(f'Соединение с сервером потеряно')
                break

    def start_rcv(self):
        receiver = threading.Thread(target=self.from_server, args=())
        receiver.daemon = True
        receiver.start()

        while True:
            time.sleep(1)
            if receiver.is_alive():
                continue
            break

    def start_send(self):
        sender = threading.Thread(target=self.to_server, args=())
        sender.daemon = True
        sender.start()

        while True:
            time.sleep(1)
            if sender.is_alive():
                continue
            break

    def start_full(self):
        receiver = threading.Thread(target=self.from_server)
        receiver.daemon = True
        receiver.start()

        sender = threading.Thread(target=self.to_server)
        sender.daemon = True
        sender.start()

        while True:
            time.sleep(1)
            if receiver.is_alive() and sender.is_alive():
                continue
            break


def main(login, addr, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((addr, port))

    client = Client(login, sock)
    client.create()
    client.start_full()


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
