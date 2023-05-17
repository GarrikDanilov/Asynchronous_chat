from subprocess import Popen


p_list = []

while True:
    command = input('Запустить клиентские приложения (s)/ Закрыть клиентские приложения (x)/ Выйти (q): ')

    if command == 'q':
        break
    elif command == 's':
        p_list.append(Popen(['x-terminal-emulator', '-e', 'python', 'client_recv.py', 'client_recv', 'localhost']))
        p_list.append(Popen(['x-terminal-emulator', '-e', 'python', 'client_send.py', 'client_send', 'localhost']))

    elif command == 'x':
        for p in p_list:
            p.kill()
        p_list.clear()