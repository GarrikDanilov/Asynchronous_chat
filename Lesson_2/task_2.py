"""
2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией 
о заказах. Написать скрипт, автоматизирующий его заполнение данными. Для этого:
1) создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), 
количество (quantity), цена (price), покупатель (buyer), дата (date). Функция должна 
предусматривать запись данных в виде словаря в файл orders.json. При записи данных указать 
величину отступа в 4 пробельных символа;
2) проверить работу программы через вызов функции write_order_to_json() с передачей в нее 
значений каждого параметра.
"""


import json


def write_order_to_json(item, quantity, price, buyer, data):
    order = {
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'data': data
    }

    with open('orders.json', 'r', encoding='utf-8') as f_in:
        orders = json.load(f_in)
    
    orders['orders'].append(order)

    with open('orders.json', 'w', encoding='utf-8') as f_out:
        json.dump(orders, f_out, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    write_order_to_json('book', 1, 500, 'Nik', '07.04.2023')
    write_order_to_json('принтер', 1, 3500, 'Иван', '07.04.2023')
