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
import time

from create_num_table import create_num_lst
from console_out import console_out as output
from give_num import give_num

def create_new_json():
    start = int(input("\nВведите начальное значение диапазона номеров: "))
    end = int(input("\nВведите конечное значение диапазона номеров: "))
    immut = input("\nДополнительно: введите неизменяемый прекфикс числа, если он пристутствует (в случае отсутствия - нажмите ввод): ")
    free_args = input("\nДополнительно+: введите через пробел дополнительные числа, по которым нужно провести выборку: ")
    if free_args:
        free_args = free_args.split()
    else:
        free_args = []
    card_num_list = create_num_lst(start, end, free_args, immut=immut)
    return card_num_list

def test_card_num(card_list):
    """
    Проверяем доступность списка с номерами. 
    """
    try:
        with open(card_list, "r") as read_file:
            test = json.load(read_file)
        return 0
    except FileNotFoundError:
        return 1
    except ValueError:
        return 2

def transit_args():
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
    return {"n": args.n, "rnd": rnd}

def main():
    timer = 5
    while True:
        main_status = test_card_num("cards_numbers.json")
        reserve_status = test_card_num("reserve_copy.json")
        if main_status == 1 and reserve_status == 0:
            with open("reserve_copy.json", "r") as read_file:
                card_num_list = json.load(read_file)
            with open("cards_numbers.json", "w") as change_file:
                json.dump(card_num_list, change_file)
            break
        elif main_status == 1:   
            card_num_list = create_new_json()
            with open("cards_numbers.json", "w") as change_file:
                json.dump(card_num_list, change_file)
            break
        
        if main_status == 0:
            break
        elif main_status == 2 and timer > 0:
            print("Файл не доступен, ожидаем ответа")
            time.sleep(2)
            timer -= 1
            continue
        else:
            raise Exception ("Системный файл недоступен или поврежден, повторите запрос позже")


    with open("cards_numbers.json", "r") as change_file:
        try:
            card_num_list = json.load(change_file)
        except ValueError:
            with open("reserve_copy.json", "r") as read_file:
                card_num_list = json.load(read_file)
    
    with open("cards_numbers.json", "w") as change_file:
        # Обрабатываем аргументы командной строки
        args = transit_args()

        # Передаю аргументы в функцию для выбора индексов
        numbers = give_num(len(card_num_list), quant=args["n"], rand=args["rnd"])  

        # Находим нужные числа по индексам в списке номеров
        for num in numbers:
            real_num = card_num_list[num]
            print("Номер для карты -", real_num)

        # Удаляем их из исходного списка
        numbers = sorted(numbers, reverse=True)  # Таким образом ошибки обращения по индексу избегаем. 
        for num in numbers:
            card_num_list.pop(num)

        print("\nДлина обработанного списка - ", len(card_num_list))

        # Сохраняем список неиспользованных номеров
        json.dump(card_num_list, change_file)

        # Создаем резервную копию данных
        with open("reserve_copy.json", "w") as write_file:
            json.dump(card_num_list, write_file)
        


if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()