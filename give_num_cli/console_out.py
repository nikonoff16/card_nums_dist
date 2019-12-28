def console_out(lst_of_nums, columns):
    """
    Функция делает косольный вывод всех номеров в том порядке, в каком они записаны в список
    :param lst_of_nums: список номеров
    :param columns: количество столбцов в выводе
    :return: функция не имеет возвращаемого значения
    """
    # Задача всей этой конструкции - вывод чисел по стобцам
    # Когда сount становится равен 0, печатается перевод строки
    if not lst_of_nums:
        print("Список пуст, невозможно его отобразить")
        return None
    count = columns - 1
    print("*" * len(lst_of_nums[0]) * columns + (columns - 1) * "*")
    for num in lst_of_nums:
        if count:
            print(num, end=' ')
            count -= 1
        else:
            count = columns - 1
            print(num)
            
    if count == columns - 1:
        print("*" * len(lst_of_nums[0]) * columns + (columns - 1) * "*")
    else:
        print("\n" + "*" * len(lst_of_nums[0]) * columns + (columns - 1) * "*")

def console_out_brief(lst_of_nums):
    if not lst_of_nums:
        print("Список пуст, невозможно его отобразить")
        return None

    diapazons = []

    prev = str(lst_of_nums[0])
    rnge = str(lst_of_nums[0])
    for num in range(1, len(lst_of_nums)):
        if int(lst_of_nums[num]) - int(prev) != 1:
            if str(prev) == rnge:
                diapazons.append(rnge)
                rnge = str(lst_of_nums[num])
            else:
                rnge += prev
                diapazons.append(rnge)
                rnge = str(lst_of_nums[num])
        else:
            if num == len(lst_of_nums):
                rnge += str(lst_of_nums[num])
                diapazons.append(rnge)
            elif rnge[-1] != '.':
                rnge += '..'
        prev = str(lst_of_nums[num])
    if ".." in rnge:
        rnge += str(lst_of_nums[-1])
    diapazons.append(rnge)
    return diapazons