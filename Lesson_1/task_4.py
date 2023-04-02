"""
4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления
в байтовое и выполнить обратное преобразование (используя методы encode и decode).
"""

var_1 = 'разработка'
var_2 = 'администрирование'
var_3 = 'protocol'
var_4 = 'standard'

print('Преобразование в байтовое представление')
in_bytes = [el.encode('utf-8') for el in (var_1, var_2, var_3, var_4)]
for item in in_bytes:
    print(item)

print('Преобразование в строковое представление')
in_str = [el.decode('utf-8') for el in in_bytes]
for item in in_str:
    print(item)
    