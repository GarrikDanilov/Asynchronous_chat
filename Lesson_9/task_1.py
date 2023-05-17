"""
1. Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться 
доступность сетевых узлов. Аргументом функции является список, в котором каждый сетевой 
узел должен быть представлен именем хоста или ip-адресом. В функции необходимо перебирать 
ip-адреса и проверять их доступность с выводом соответствующего сообщения («Узел доступен», 
«Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().
"""


from ipaddress import ip_address
from subprocess import check_call, PIPE, CalledProcessError


def host_ping(list_addresses, requests=1):
    reachable = []
    unreachable = []
    for address in list_addresses:
        try:
            address = ip_address(address)
        except ValueError:
            pass
        try:
            check_call(f'ping -c {requests} {address}'.split(), stdout=PIPE)
            reachable.append(str(address))
        except CalledProcessError:
            unreachable.append(str(address))
    return reachable, unreachable


if __name__ == '__main__':
    ip_adresses = ['yandex.ru', 'youtube.com', '2.2.2.2']
    reachable, unreachable = host_ping(ip_adresses)
    for address in reachable:
        print(f'Узел {address} доступен')
    for address in unreachable:
        print(f'Узел {address} недоступен')

"""
Узел yandex.ru доступен
Узел youtube.com доступен
Узел 2.2.2.2 недоступен
"""
