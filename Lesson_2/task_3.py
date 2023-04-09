"""
3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение 
данных в файле YAML-формата. Для этого:
1) подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, 
второму — целое число, третьему — вложенный словарь, где значение каждого ключа — это целое 
число с юникод-символом, отсутствующим в кодировке ASCII (например, €);
2) реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом 
обеспечить стилизацию файла с помощью параметра default_flow_style, а также установить возможность 
работы с юникодом: allow_unicode = True;
3) реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
"""


import yaml


data_write = {
    'key_1': ['item1', 'item2', 3],
    'key_2': 5,
    'key_3': {
        'first': '1€',
        'second': '2₽',
        'third': '3₿'
    }
}

with open('file.yaml', 'w', encoding='utf-8') as f_out:
    yaml.safe_dump(data_write, f_out, default_flow_style=False, allow_unicode=True, 
                   sort_keys=False)
    
with open('file.yaml', 'r', encoding='utf-8') as f_in:
    data_load = yaml.safe_load(f_in)

print(data_write == data_load)
    