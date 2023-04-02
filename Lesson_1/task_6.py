"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование»,
«сокет», «декоратор». Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате
Unicode и вывести его содержимое.
"""

test_str = ('сетевое программирование', 'сокет', 'декоратор')
with open('test_file.txt', 'w') as f_out:
    for line in test_str:
        f_out.write(f'{line}\n')
print(f'Кодировка файла по умолчанию - {f_out.encoding}.\n')

with open('test_file.txt', encoding='utf-8') as f_in:
    try:
        for line in f_in:
            print(line)
    except UnicodeDecodeError as er:
        print(f'Ошибка декодирования: {er}')

# Открытие файла в правильной кодировке
print(f'\nОткрытие файла в правильной кодировке:')
with open('test_file.txt', encoding=f_out.encoding) as f_in:
    for line in f_in:
        print(line)
