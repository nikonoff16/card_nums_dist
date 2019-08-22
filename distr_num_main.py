"""
Скрипт проверяет налчие файла с номерами.
Если нет - создает новый, вызывая модуль create_num_table.py,
запрашивая у пользователя параметры создания номеров карт.
Если да - подключает найденный json-файл, извлекает из него информацию, 
выдает очередной номер (случайным образом полученный из множества оставшихся номеров),
удаляет его из списка и помещает в список использованных номеров. 
После выполнения этой работы производится запись в json-файл с номерами. 
"""
import json
from create_num_table import create_num_lst
from console_out import console_out as output


try:
    with open("cards_numbers.json", "r") as read_file:
        card_num_list = json.load(read_file)
except FileNotFoundError:

    print("Похоже, что файла с номерами не существует. Для продолжения работы нужно будет создать такой файл.")
    start = int(input("Введите начальное значение диапазона номеров: "))
    end = int(input("Введите конечное значение диапазона номеров: "))
    immut = input("Введите неизменяемый прекфикс числа, если он пристутствует (в случае отсутствия - нажмите ввод): ")
    free_args = input("Введите через пробел дополнительные числа, по которым нужно провести выборку: ")
    if free_args:
        free_args = free_args.split()
    else:
        free_args = []

    card_num_list = create_num_lst(start, end, free_args, immut=immut)
    # TODO: Нижележащий модуль не нужен, так как запись будем производить из списка в конце работы программы
    with open("cards_numbers.json", "w") as write_file:
        json.dump(card_num_list, write_file)

# TODO: сделать обработчик аргументов командной строки
output(card_num_list, 10)

