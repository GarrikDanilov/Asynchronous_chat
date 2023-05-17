import sys
import argparse
import socket
import time
import threading
import logging
import common
import log.client_log_config
from decos import log


class ServerError(Exception):
    pass


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
    parser.add_argument('login', help='Логин')
    parser.add_argument('addr', help='IP-адрес сервера')
    parser.add_argument('port', nargs='?', default=common.DEFAULT_PORT, type=int, 
                        help=f'TCP-порт на сервере, по умолчанию {common.DEFAULT_PORT}')
    
    args = parser.parse_args()
    if args.port < 1024 or args.port > 65535:
        logger.error(f'Некорректный номер порта - {args.port}. Номер порта должен быть \
в диапазоне от 1024 до 65535')
        sys.exit(1)     

    return args.login, args.addr, args.port 


def to_server(sock, login):
    while True:
        command = input('Отправить сообщение (s)/ Выйти (q): ')

        if command == 'q':
            sock.close()
            break
        elif command == 's':
            to_client = input('Введите получателя: ')
            message = input('Введите сообщение: ')

            try:
                common.send_msg(create_msg(to_client, login, message), sock)
            except:
                logger.critical(f'Соединение с сервером потеряно')
                break


def from_server(sock):
    while True:
        try:
            message = common.get_msg(sock)
            if 'response' in message:
                print(f'\nОшибка: {message["error"]}')
            else:
                print(f'\n{message["from"]}: {message["message"]}')
        except:
            logger.critical(f'Соединение с сервером потеряно')
            break


def main(login, addr, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((addr, port))

    common.send_msg(create_presence(login, 'active'), sock)
    msg_from_server = common.get_msg(sock)
    if msg_from_server['response'] == 400:
        raise ServerError(msg_from_server['error'])
    logger.info('Соединение с сервером установлено')

    receiver = threading.Thread(target=from_server, args=(sock, ))
    receiver.daemon = True
    receiver.start()

    sender = threading.Thread(target=to_server, args=(sock, login))
    sender.daemon = True
    sender.start()

    while True:
        time.sleep(1)
        if receiver.is_alive() and sender.is_alive():
            continue
        break


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
