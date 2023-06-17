import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QTableView, QDialog, \
    QPushButton, QLineEdit, QFileDialog
from PyQt6.QtGui import QAction, QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt


def create_user_model(db):
    list_users = db.get_user()
    list = QStandardItemModel()
    list.setHorizontalHeaderLabels(['ID клиента', 'Логин', 'Дата последнего соединения'])
    for row in list_users:
        id, login, date = row
        id = QStandardItem(str(id))
        id.setEditable(False)
        login = QStandardItem(login)
        login.setEditable(False)
        date = QStandardItem(date.strftime('%d.%m.%y %H:%M:%S'))
        date.setEditable(False)
        list.appendRow([id, login, date])
    return list


def create_history_model(db):
    hist_list = db.get_history()

    list = QStandardItemModel()
    list.setHorizontalHeaderLabels(['Логин', 'Дата последнего соединения', 'IP адрес'])
    for row in hist_list:
        login, date, ip_address = row
        login = QStandardItem(login)
        login.setEditable(False)
        date = QStandardItem(date.strftime('%d.%m.%y %H:%M:%S'))
        date.setEditable(False)
        ip_address = QStandardItem(ip_address)
        ip_address.setEditable(False)
        list.appendRow([login, date, ip_address])
    return list


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        exitAction = QAction('Выйти', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(QApplication.quit)

        self.refresh_btn = QAction('Обновить', self)

        self.conf_btn = QAction('Настройки', self)

        self.stat_btn = QAction('Статистика', self)

        self.statusBar()
        self.toolbar = self.addToolBar('MainBar')
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(self.refresh_btn)
        self.toolbar.addAction(self.conf_btn)
        self.toolbar.addAction(self.stat_btn)

        self.setFixedSize(800, 600)
        self.setWindowTitle('Admin')

        self.lable = QLabel('Список клиентов:', self)
        self.lable.setFixedSize(240, 15)
        self.lable.move(10, 35)

        self.clients_table = QTableView(self)
        self.clients_table.setFixedSize(780, 400)
        self.clients_table.move(10, 55)

        self.show()


class HistoryWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Статистика клиентов')
        self.setFixedSize(600, 700)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.close_btn = QPushButton('Закрыть', self)
        self.close_btn.move(250, 650)
        self.close_btn.clicked.connect(self.close)

        self.history_table = QTableView(self)
        self.history_table.move(10, 10)
        self.history_table.setFixedSize(580, 620)

        self.show()


class ConfigWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(365, 260)
        self.setWindowTitle('Настройки сервера')

        self.db_path_label = QLabel('Путь до файла базы данных: ', self)
        self.db_path_label.move(10, 10)
        self.db_path_label.setFixedSize(240,15)

        self.db_path = QLineEdit(self)
        self.db_path.setFixedSize(250, 20)
        self.db_path.move(10, 30)
        self.db_path.setReadOnly(True)
        
        self.db_path_select = QPushButton('Обзор', self)
        self.db_path_select.move(275, 28)

        def open_file_dialog():
            global dialog
            dialog = QFileDialog(self)
            path = dialog.getExistingDirectory()
            self.db_path.clear()
            self.db_path.insert(path)

        self.db_path_select.clicked.connect(open_file_dialog)

        self.db_file_label = QLabel('Имя файла базы данных: ', self)
        self.db_file_label.move(10, 68)
        self.db_file_label.setFixedSize(180,15)

        self.db_file = QLineEdit(self)
        self.db_file.setFixedSize(150, 20)
        self.db_file.move(200, 66)

        self.port_label = QLabel('Номер порта: ', self)
        self.port_label.move(10, 108)
        self.port_label.setFixedSize(180, 15)

        self.port = QLineEdit(self)
        self.port.setFixedSize(150, 20)
        self.port.move(200, 108)

        self.ip_label = QLabel('IP адрес: ', self)
        self.ip_label.move(10, 148)
        self.ip_label.setFixedSize(180, 15)

        self.ip_label_note = QLabel('Оставьте поле пустым, чтобы\nпринимать соединения с любых адресов', self)
        self.ip_label_note.move(10, 168)
        self.ip_label_note.setFixedSize(500, 30)

        self.ip = QLineEdit(self)
        self.ip.setFixedSize(150, 20)
        self.ip.move(200, 148)

        self.save_btn = QPushButton('Сохранить', self)
        self.save_btn.move(250, 220)

        self.close_btn = QPushButton('Закрыть', self)
        self.close_btn.move(20, 220)
        self.close_btn.clicked.connect(self.close)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    config_window = ConfigWindow()
    sys.exit(app.exec())
