from subprocess import Popen


p_list = []

while True:
    command = input('Запустить сервер и клиентов (s)/ Закрыть клиентов (x)/ Выйти (q): ')

    if command == 'q':
        break
    elif command == 's':
        p_list.append(Popen(['x-terminal-emulator', '-e', 'python', 'server_select.py']))

        for _ in range(2):
            p_list.append(Popen(['x-terminal-emulator', '-e', 'python', 'client_send.py', 'localhost']))

        for _ in range(2):
            p_list.append(Popen(['x-terminal-emulator', '-e', 'python', 'client_recv.py', 'localhost']))

    elif command == 'x':
        for p in p_list:
            p.kill()
        p_list.clear()
        