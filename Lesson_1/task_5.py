"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в строковый тип
на кириллице.
"""

import subprocess


args_yandex = ['ping', 'yandex.ru']
args_youtube = ['ping', 'youtube.com']

# пинг yandex.ru
subproc_ping = subprocess.Popen(args_yandex, stdout=subprocess.PIPE)
for line in subproc_ping.stdout:
    line = line.decode('cp866').encode('utf-8')
    print(line.decode('utf-8'))

# пинг youtube.com
subproc_ping = subprocess.Popen(args_youtube, stdout=subprocess.PIPE)
for line in subproc_ping.stdout:
    line = line.decode('cp866').encode('utf-8')
    print(line.decode('utf-8'))
