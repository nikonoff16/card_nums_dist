def console_out(lst_of_nums, columns):
    """
    Функция делает косольный вывод всех номеров в том порядке, в каком они записаны в список
    :param lst_of_nums: список номеров
    :param columns: количество столбцов в выводе
    :return: функция не имеет возвращаемого значения
    """
    count = columns
    for num in lst_of_nums:
        if count:
            print(num, end=' ')
            count -= 1
        else:
            count = columns
            print(num)