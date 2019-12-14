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
import sys
import argparse

from create_num_table import create_num_lst
from console_out import console_out as output
from give_num import give_num

def main():
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
        # # TODO: Нижележащий модуль не нужен, так как запись будем производить из списка в конце работы программы
        # with open("cards_numbers.json", "w") as write_file:
        #     json.dump(card_num_list, write_file)
    
    # Проверяем наличие файла с отработанными нормерами
    try:
        with open("distr_numbers.json", "r") as read_file:
            distr_num_list = json.load(read_file)
    except FileNotFoundError:
        print("Файл использованных номеров не найден, создается новый...")
        distr_num_list = []

    # Обрабатываем аргументы командной строки
    parser = argparse.ArgumentParser(description="Numbers of card numbers and some other data.")
    parser.add_argument("--n", type=int, default=1, help="Необязательный аргумент - количество номеров.")
    parser.add_argument("--rnd", type=int, default=1, help="Необязательный аргумент - количество номеров.")
    args = parser.parse_args()

    # Костыль, обрабатываю один из необязательных аргументов
    if args.rnd != 0:
        rnd = True
    else:
        rnd = False

    # Передаю аргументы в функцию для выбора индексов
    numbers = give_num(len(card_num_list), args.n, rand=rnd)  

    # Находим нужные числа по индексам в списке номеров
    for num in numbers:
        real_num = card_num_list[num]
        distr_num_list.append(card_num_list[num])
        print("Номер для карты -", real_num)

    # Удаляем их из исходного списка
    numbers = sorted(numbers, reverse=True)  # Таким образом ошибки обращения по индексу избегаем. 
    for num in numbers:
        card_num_list.pop(num)

    print("\n", len(card_num_list), "- длина обработанного списка")

    # Готовимся к сохранению информации на диск
    # Сохраняем список неиспользованных номеров
    with open("cards_numbers.json", "w") as write_file:
        json.dump(card_num_list, write_file)

    # Сохраняем список использованных номеров
    with open("distr_numbers.json", "w") as write_file:
        json.dump(distr_num_list, write_file)


if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()