import socket
import select
import time
import common
from server import logger, get_args, create_response, new_listen_socket


def main(addr, port):
    sock = new_listen_socket(addr, port)

    clients = []
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
                    elif msg_from_client['action'] == 'msg':
                        messages.append((msg_from_client['from'], msg_from_client['message']))
                except:
                    logger.info(f'Клиент {client.getpeername()} отключился от сервера')
                    clients.remove(client)

        if messages and w_clients:
            msg = {
                'action': 'msg',
                'time': time.time(),
                'from': messages[0][0],
                'message': messages[0][1]
            }
            del messages[0]
            for client in w_clients:
                try:
                    common.send_msg(msg, client)
                except:
                    logger.info(f'Клиент {client.getpeername()} отключился от сервера')
                    clients.remove(client)


if __name__ == '__main__':
    addr, port = get_args()
    main(addr, port)
