"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование»,
«сокет», «декоратор». Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате
Unicode и вывести его содержимое.
"""

from chardet.universaldetector import UniversalDetector


Detector = UniversalDetector()
with open('test_file.txt', 'rb') as f:
    for line in f:
        Detector.feed(line)
        if Detector.done:
            break
    Detector.close()
print(f'Кодировка файла по умолчанию - {Detector.result["encoding"]}.\n')
# Кодировка файла по умолчанию - cp1251.

try:
    with open('test_file.txt', encoding='utf-8') as f_in:
        for line in f_in:
            print(line)
except UnicodeDecodeError as er:
    print(f'Ошибка декодирования: {er}')
# В случае отличия кодировки возникнет ошибка декодирования: 'utf-8' codec can't decode byte 0xf1 in position 0: invalid continuation byte

# Открытие файла в правильной кодировке
print(f'\nОткрытие файла в правильной кодировке:')
with open('test_file.txt', encoding=Detector.result['encoding']) as f_in:
    for line in f_in:
        print(line)
