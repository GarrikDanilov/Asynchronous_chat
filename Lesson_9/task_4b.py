from subprocess import Popen


p_list = []

while True:
    command = input('Запустить клиентские приложения (s)/ Закрыть клиентские приложения (x)/ Выйти (q): ')

    if command == 'q':
        break
    elif command == 's':
        num_proc = int(input('Введите количество клиентских приложений: '))

        for _ in range(num_proc):
            p_list.append(Popen(['x-terminal-emulator', '-e', 'python', 'client.py', f'client{num_proc + 1}', 'localhost']))

    elif command == 'x':
        for p in p_list:
            p.kill()
        p_list.clear()