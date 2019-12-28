import json
import sys
import argparse
import time

from create_num_table import create_num_lst
from console_out import console_out as output
from distribute_num import distribute_num

def create_new_json():
    """
    Функция создает новый файл с нужными параметрами. Странная система префиксов и дополнительных чисел
    исходит из местечковой специфики бумажных списков, используемых в больнице, где работал создатель
    скрипта. Часто приходилось довольствоваться маленьким куском от большого списка, который жил именно по
    своим правилам: имел только числа, оканчивающиеся на 1, 2, 3, а начинающийся с условного 456. Найдя такие 
    закономерности, можно перенести любое бумажное безобразие в красивые электронные списки. 
    """
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
    """
    Обрабатываем аргументы командной строки отдельной функцией
    """
    parser = argparse.ArgumentParser(description="Утилита для получения номера медицинской карты. ")
    parser.add_argument("-n", "--nums", type=int, default=1, help="Указывает количество нужных номеров карт")
    parser.add_argument("-r", "--random", action="store_true", help="Программа выбирает номера в случайном порядке")
    parser.add_argument("-a", "--append", action="store_true", help="Открывает диалог дополнения списка")
    parser.add_argument("-v", "--verbose", action="store_true", help="Вывод на экран всего оставшегося списка номеров")
    args = parser.parse_args()

    # # Костыль, обрабатываю один из необязательных аргументов
    # if args.rnd != 0:
    #     rnd = True
    # else:
    #     rnd = False
    # return {"n": args.n, "rnd": rnd, "v": args.v}
    return args

def main():
    """ 
    Тело главной функции. Аргументов не принимает. 
    При множественных вызовах этой функции уникальность раздаваемых номеров гарантируется блокировой файла 
    с номерами. Блокировка заключается в том, что файл становится пустым, и при любом обращении к нему из 
    другой программы обработчик json-файлов получает ValueError. Эта ошибка ловится и программа повторяет 
    обращение к файлу через некоторое время. 
    TODO: Если количество_пользователей > 20: 
               блокировка_с_задержкой = использование_БД  # или иной масштабируемый способ
    """

    # блок проверки наличия, доступности и восстановления файла
    # TODO: прикрутить восстановление, если файл пуст. 
    timer = 5
    while True:
        main_status = test_card_num("cards_numbers.json")
        reserve_status = test_card_num("reserve_copy.json")
        if main_status == 1 and reserve_status == 0:    # Если нет файла с номерами, но есть его копия
            with open("reserve_copy.json", "r") as read_file:
                card_num_list = json.load(read_file)
            with open("cards_numbers.json", "w") as change_file:
                json.dump(card_num_list, change_file)
            break
        elif main_status == 1:                          # Если файла с номерами нет ни в каком виде
            card_num_list = create_new_json()
            with open("cards_numbers.json", "w") as change_file:
                json.dump(card_num_list, change_file)
                print("\nПолный список созданных номеров для карт:\n")
                print(f"С хуйбалы {card_num_list[0]} по {card_num_list[-1]}")
                output(card_num_list, 10)
            break
        
        if main_status == 0:
            break
        elif main_status == 2 and timer > 0:            # То есть если ValueError
            print("Файл не доступен, ожидаем ответа")
            time.sleep(2)
            timer -= 1
            continue
        else:
            print("Системный файл недоступен или поврежден, повторите запрос позже")
            exit()

    # Обрабатываем аргументы командной строки
    args = transit_args()

    # Считываем данные из файла с номерами. 
    # TODO: Срочно поменять эту систему. Файл может стать заблокированным в момент между 
    # проверкой и записью, и тогда уникальность номеров может быть скомпроментирована. 
    with open("cards_numbers.json", "r") as change_file:
        card_num_list = json.load(change_file)
        if args.append:
            print("Добавляем новые номера в конец старого списка. Следуйте инструкциям в терминале:")
            new_nums = create_new_json()
            card_num_list += new_nums
    
    if card_num_list:  # Недопускаем работы с пустым списком. 
        # Блокируем файл, выдаем пользователю номера, производим запись в основной и резервный файлы. 
        with open("cards_numbers.json", "w") as change_file:

            # Передаю аргументы в функцию для выбора индексов
            numbers = distribute_num(len(card_num_list), quant=args.nums, rand=args.random)  

            # Находим нужные числа по индексам в списке номеров
            print("\n" + "*" * (18 + len(card_num_list[0])))
            for num in numbers:
                real_num = card_num_list[num]
                # здесь записываем выданные номера в виде строки. 
                with open("archive_nums.txt", "a") as old_nums:
                    old_nums.write(real_num + " ")
                print("Номер для карты -", real_num)
            print("*" * (18 + len(card_num_list[0])))

            # Удаляем их из исходного списка
            numbers = sorted(numbers, reverse=True)  # Таким образом ошибки обращения по индексу избегаем. 
            for num in numbers:
                card_num_list.pop(num)

            print("\nДлина обработанного списка - ", len(card_num_list))

            # Выводим все номера на экран, если аргумент --v отличается от 0
            # Аргумент --v определяет количество столбцов, в которое будет показан список
            if args.verbose:
                print("\nПолный список оставшихся номеров для карт:\n")
                print(f"С хуйбалы {card_num_list[0]} по {card_num_list[-1]}")
                output(card_num_list, 10)

            # Сохраняем список неиспользованных номеров
            json.dump(card_num_list, change_file)

            # Создаем резервную копию данных
            with open("reserve_copy.json", "w") as write_file:
                json.dump(card_num_list, write_file)
    else:
        print("Список свободных номеров пуст. запустите утилиту с аргументом -a (--append) для пополнения списка номеров.")   


if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()