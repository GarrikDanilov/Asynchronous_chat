"""sumary_line
1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку 
определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый 
«отчетный» файл в формате CSV. Для этого:
    1) создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, 
    их открытие и считывание данных. В этой функции из считанных данных необходимо с помощью 
    регулярных выражений извлечь значения параметров «Изготовитель системы», «Название ОС», 
    «Код продукта», «Тип системы». Значения каждого параметра поместить в соответствующий список. 
    Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list, 
    os_type_list. В этой же функции создать главный список для хранения данных отчета — например, 
    main_data — и поместить в него названия столбцов отчета в виде списка: «Изготовитель системы», 
    «Название ОС», «Код продукта», «Тип системы». Значения для этих столбцов также оформить в виде 
    списка и поместить в файл main_data (также для каждого файла);
    2) создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. 
    В этой функции реализовать получение данных через вызов функции get_data(), а также 
    сохранение подготовленных данных в соответствующий CSV-файл;
    3) проверить работу программы через вызов функции write_to_csv().
"""


import csv
import re


def get_data():
    headers = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    os_prod_reg = re.compile(r'Изготовитель системы:\s*\S*')
    os_name_reg = re.compile(r'Название ОС:\s*\S*')
    os_code_reg = re.compile(r'Код продукта:\s*\S*')
    os_type_reg = re.compile(r'Тип системы:\s*\S*')

    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = [headers]

    for i in range(1, 4):
        with open(f'info_{i}.txt', 'r', encoding='utf-8') as f_in:
            data = f_in.read()
        
        os_prod_list.append(os_prod_reg.findall(data)[0].split()[2])
        os_name_list.append(os_name_reg.findall(data)[0].split()[2])
        os_code_list.append(os_code_reg.findall(data)[0].split()[2])
        os_type_list.append(os_type_reg.findall(data)[0].split()[2])

    for row in zip(os_prod_list, os_name_list, os_code_list, os_type_list):
        main_data.append(list(row))
    
    return main_data


def write_to_csv(file_name):
    data = get_data()
    with open(file_name, 'w', encoding='utf-8') as f_out:
        writer = csv.writer(f_out, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerows(data)


if __name__ == '__main__':
    write_to_csv('report.csv')
