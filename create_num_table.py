def cnt_zs(greater_num, lesser_num):
    """
    Функция считает количество нулей, которое нужно вставить перед числом, чтобы оно соответствовало
    заданному формату номера. Это актуально в случае, если при выполнении функции create_num_lst()
    указан некий префикс - тогда все числа будут одинаковой длины, заданная разрядность номеров будет
    сохранена
    :param greater_num: целое число, предельное для указанной последовательности
    :param lesser_num: целое число, которое с предельным сравнивается
    :return: строка, содержащая такое количество нулей, которое дополнит число до нужной разрядности;
             может быть пустой строкой, если числа одинаковой длины.
    """
    zeros = ''
    ln_zeros = len(str(greater_num)) - len(str(lesser_num))
    return zeros + ('0' * ln_zeros)


def create_num_lst(start, end, args, immut=''):
    """
    Функция создает список номеров по указанным параметрам.
    Примерный use case: есть список на бумаге, известны правила
    его построения, но переписывать его от руки работа бестолковая и кропотливая.
    В таком случае нужно найти неизменяемую часть, указать начало и конец изменяемой части,
    и в дополнительные элементы args через запятую прописать правила отбора чисел
    (например, чтобы последние цифры были только 1, 2 и 3, или 20, 30, 40).
    Если не указать аргументов отбора чисел, то будут добавлены в список все числа
    последовательности, ограниченной аргументами start и end.
    :param start: целое число, точка отсчета для поиска новых чисел
    :param end: целое число, за которым поиск уже не осуществляется
    :param args: список из элементов, на основании которых будет происходить сортировка;
    при пустом списке сортировка не производится
    :param immut: строка, префикс, который будет добавляться к каждому числу; по умолчанию - пустая строка
    :return: список из созданных номеров
    """
    result = []

    for number in range(start, end+1):          # единица добавлена, чтобы пользователь получал ровно то, что ввел
        # Если нет свободных аргументов, то добавлять все числа
        if not args:
            result.append(str(immut + cnt_zs(end, number) + str(number)))
        else:
            for free_arg in args:
                # Проверяет последние цифры числа на соответствие со свободными аргументам
                if str(number)[-int((len(free_arg))):] in args:
                    result.append(str(immut + cnt_zs(end, number) + str(number)))
                    break
    return result



