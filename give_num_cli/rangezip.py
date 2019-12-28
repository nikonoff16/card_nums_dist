__version__ = "0.2.1"


def ziprange(list_):
    '''
    :param list_: list of strings with valid ints
    :return: list of string with ranges
    '''
    ranges_list = []
    cnt = 0
    first = None

    while True:
        try:
            current = int(list_[cnt])
            next = int(list_[cnt+1])
        except IndexError:
            break

        if not first:
            first = current

        if current+1 != next:
            ranges_list.append(f"{first}...{current}")
            if first == current:
                ranges_list[-1] = str(current)
            first = None

        cnt += 1

    ranges_list.append(f"{first}...{current}")
    if first is None:
        ranges_list[-1] = str(current)

    return ranges_list

if __name__ == '__main__':
    print("Tests:")
    print(ziprange([-10, "1","2","3", "100", "202", "203", "204", "300"]) ==
                   ['-10', '1...3', "100", '202...204', "300"])
    print(ziprange([-10, "1","2","3", "100", "202", "203", "204"]) ==
                   ['-10', '1...3', "100", '202...204'])
    print(ziprange(["1", "2", "3", "100", "202", "203", "204"]) ==
                   ['1...3', "100", '202...204'])