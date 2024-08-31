import random


class Results:
    WIN = "WIN"
    LOSS = "LOSS"
    DRAW = "DRAW"


def res():
    list1 = [random.randint(1, 11), random.randint(1, 11)]
    list2 = [random.randint(1, 11), random.randint(1, 11)]

    print(f"Карты дилера: ? {list1[1]}")
    print(f"Ваши карты: {list2[0]} {list2[1]}")
    sum2 = sum(list2)

    choice = 1
    i = 2
    while choice == 1:
        print("Тянете еще карту?")
        print("1 - Да")
        print("0 - Нет")
        choice = int(input("Ввод: "))
        if choice == 1:
            list2.append(random.randint(1, 9))
            sum2 += list2[i]
            print(f"Вы вытянули {list2[i]}")
            print(f"Ваши карты: {' '.join(map(str, list2))}")

            if sum2 > 21:
                return Results.LOSS
            elif sum2 == 21:
                return Results.WIN
            i += 1
        else:
            break

    print(f"Карты дилера: {' '.join(map(str, list1))}")

    sum1 = sum(list1)
    i = 2
    while True:
        list1.append(random.randint(1, 9))
        sum1 += list1[i]
        print(f"Дилер вытянул {list1[i]}")
        print(f"Карты дилера: {' '.join(map(str, list1))}")

        if sum1 > 21:
            return Results.WIN
        elif sum1 > sum2:
            return Results.LOSS
        elif sum1 == sum2:
            return Results.DRAW
        i += 1


def main():
    random.seed()
    results = res()

    if results == Results.WIN:
        print("Вы победили")
    elif results == Results.LOSS:
        print("Вы проиграли")
    elif results == Results.DRAW:
        print("Ничья")


if __name__ == "__main__":
    main()
