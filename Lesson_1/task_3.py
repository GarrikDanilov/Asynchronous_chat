"""
3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
"""

var_1 = 'attribute'
var_2 = 'класс'
var_3 = 'функция'
var_4 = 'type'

for var in (var_1, var_2, var_3, var_4):
    try:
        bytes(var, 'ascii')
    except UnicodeEncodeError:
        print(f'"{var}" - невозможно записать в байтовом типе.')
