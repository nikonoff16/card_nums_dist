from random import randint

def distribute_num(lst_len, quant=1, rand=False):
    chosen_nums = []
    # Этот код ограничивает количество запрошенных чисел, если оно превосходит количество чисел в списке
    if quant > lst_len:
        quant = lst_len

    if not rand:
        for num in range(0, quant):
            chosen_nums.append(num)
    else:
        while quant > 0:
            num = randint(0, lst_len-1)
            if num not in chosen_nums:
                chosen_nums.append(num)
                quant -= 1
            else:
                # print("Число", num, "уже есть в списке.")
                continue
    return chosen_nums

# print(sorted(give_num(10, 21)))
# print(give_num(20, 600, rand=False))
