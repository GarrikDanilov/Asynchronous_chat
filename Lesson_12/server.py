import os
import sys
import argparse
import configparser
import logging
import socket
import select
import time
import threading
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer
from common import DEFAULT_PORT, MAX_CONNECTIONS, MAX_TIMEOUT, send_msg, get_msg
import log.server_log_config
from decos import Log
from descriptors import ValidatingPort
from metaclasses import ServerVerifier
from server_storage import ServerStorage
import server_gui as gui


logger = logging.getLogger('server')

new_connection = False
conflag_lock = threading.Lock()


class NotFoundError(Exception):
    pass


def get_args(default_port, default_address):
    parser = argparse.ArgumentParser(description='Server script')
    parser.add_argument('-p', dest='port', default=default_port, type=int)
    parser.add_argument('-a', dest='addr', default=default_address)
    
    args = parser.parse_args(sys.argv[1:])    

    return args.addr, args.port


class Server(threading.Thread, metaclass=ServerVerifier):
    port = ValidatingPort(logger)

    def __init__(self, addr, port, database):
        self.addr = addr
        self.port = port
        self.db = database
        self.clients = []
        self.logins = dict()
        self.messages = []
        self.commands = []

        super().__init__()
    
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
        
    def process_commands(self, command, socks):
        if command['action'] == 'add_contact':
            self.db.add_contact(command['user_login'], command['user_id'])
            out_msg = {'response': 202}
        elif command['action'] == 'del_contact':
            self.db.del_contact(command['user_login'], command['user_id'])
            out_msg = {'response': 202}
        elif command['action'] == 'get_contacts':
            contacts = self.db.get_contacts(command['user_login'])
            out_msg = {
                'response': 202,
                'alert': contacts
            }

        if self.logins[command['user_login']] not in socks:
            raise ConnectionError
        
        send_msg(out_msg, self.logins[command['user_login']])
    
    def run(self):
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
                            login = msg_from_client['user']['account_name']
                            ip, _ = client.getpeername()
                            self.logins[login] = client
                            self.db.log_in(login)
                            self.db.add_history(login, ip)
                        elif msg_from_client['action'] == 'msg':
                            self.messages.append(msg_from_client)
                        else:
                            self.commands.append(msg_from_client)
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

            for command in self.commands:
                try:
                    self.process_commands(command, w_clients)
                except ConnectionError:
                    logger.info(f'Клиент {command["user_login"]} отключился от сервера')
                    self.clients.remove(self.logins[command["user_login"]])
                    del self.logins[command["user_login"]]
            self.commands.clear()


def main():
    config = configparser.ConfigParser()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config.read(f"{dir_path}/{'server.ini'}")
    
    addr, port = get_args(config['SETTINGS']['default_port'], 
                          config['SETTINGS']['listen_address'])
    
    full_path = os.path.join(config['SETTINGS']['db_path'], 
                                                 config['SETTINGS']['db_file'])

    db = ServerStorage(f"sqlite:///{full_path}")

    server = Server(addr, port, db)
    server.daemon = True
    server.start()

    admin_gui = QApplication(sys.argv)
    main_window = gui.MainWindow()
    main_window.statusBar().showMessage('Server working')
    main_window.clients_table.setModel(gui.create_user_model(db))
    main_window.clients_table.resizeColumnsToContents()
    main_window.clients_table.resizeRowsToContents()

    def list_update():
        global new_connection
        if new_connection:
            main_window.clients_table.setModel(gui.create_user_model(db))
            main_window.clients_table.resizeColumnsToContents()
            main_window.clients_table.resizeRowsToContents()
        with conflag_lock:
            new_connection = False

    def show_stat():
        global stat_window
        stat_window = gui.HistoryWindow()
        stat_window.history_table.setModel(gui.create_history_model(db))
        stat_window.history_table.resizeColumnsToContents()
        stat_window.history_table.resizeRowsToContents()
        stat_window.show()

    def server_config():
        global config_window
        config_window = gui.ConfigWindow()
        config_window.db_path.insert(config['SETTINGS']['db_path'])
        config_window.db_file.insert(config['SETTINGS']['db_file'])
        config_window.port.insert(config['SETTINGS']['default_port'])
        config_window.ip.insert(config['SETTINGS']['listen_address'])
        config_window.save_btn.clicked.connect(save_server_config)

    def save_server_config():
        global config_window
        message = QMessageBox()
        config['SETTINGS']['db_path'] = config_window.db_path.text()
        config['SETTINGS']['db_file'] = config_window.db_file.text()
        try:
            port = int(config_window.port.text())
        except ValueError:
            message.warning(config_window, 'Ошибка', 'Порт должен быть числом')
        else:
            config['SETTINGS']['listen_address'] = config_window.ip.text()
            if 1023 < port < 65536:
                config['SETTINGS']['default_port'] = str(port)
                with open(f"{dir_path}/{'server.ini'}", 'w') as conf:
                    config.write(conf)
                    message.information(config_window, 'ОК', 'Настройки успешно сохранены')
            else:
                message.warning(config_window, 'Ошибка', 'Порт должен быть от 1024 до 65536')
    
    timer = QTimer()
    timer.timeout.connect(list_update)
    timer.start(1000)

    main_window.refresh_btn.triggered.connect(list_update)
    main_window.stat_btn.triggered.connect(show_stat)
    main_window.conf_btn.triggered.connect(server_config)

    admin_gui.exec()


if __name__ == '__main__':
    main()
