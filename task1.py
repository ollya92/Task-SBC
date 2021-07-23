import math

# открываем файл input.txt для чтения

with open("INPUT.txt", "r", encoding="cp1251") as infile:
    # считываем данные для расчета

    # формируем список
    n = infile.read().splitlines()

    # высота частокола
    height_N = int(n[0])

    # количество колов в частоколе
    count_M = int(n[1])

    # высота деревьев
    height_tree_H = int(n[2])

    # проверяем правильность исходных данных и производим расчет
    if 1 <= height_N <= height_tree_H and 1 <= count_M <= 100:

        # количество целых кольев на одно дерево
        kol_per_tree = height_tree_H // height_N

        # минимальное количество деревьев под сруб
        tree_needed = math.ceil(count_M / kol_per_tree)

        # запись результата в файл output.txt
        with open('OUTPUT.txt', 'w') as outfile:
            outfile.write(str(tree_needed))

    else:
        print("Your values are wrong!")
