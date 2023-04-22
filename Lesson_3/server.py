import argparse
import socket
import time
import common


def create_response(msg):
    if 'action' in msg and msg['action'] == 'presence':
        return {
            'response': 200,
            'time':time.time(),
            'alert': '200, OK'
        }
    
    return {
        'response': 400,
        'time':time.time(),
        'error': '400, Bad request'
    }


def main(addr, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((addr, port))
    sock.listen(common.MAX_CONNECTIONS)

    while True:
        client, addr = sock.accept()
        msg_from_client = common.get_msg(client)
        print(msg_from_client)
        msg_to_client = create_response(msg_from_client)
        common.send_msg(msg_to_client, client)
        client.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Server script')
    parser.add_argument('-p', dest='port', default=common.DEFAULT_PORT, type=int, 
                        help=f'TCP-порт, по умолчанию {common.DEFAULT_PORT}')
    parser.add_argument('-a', dest='addr', default='', 
                        help='IP-адрес для прослушивания, по умолчанию все доступные адреса')
    try:
        args = parser.parse_args()
        if args.port < 1024 or args.port > 65535:
            raise ValueError

        main(args.addr, args.port)
    except ValueError:
        print(f'Номер порта должен быть в диапазоне от 1024 до 65535')
