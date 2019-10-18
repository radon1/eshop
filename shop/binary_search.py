def binary_search(list, item):      #В переменных low and high хранятся границы той части списка, в которой выполняется поиск
    low = 0
    high = len(list) - 1

    while low <= high:      #Пока эта часть не сократиться до одного элемента
        mid = low + high    #....проверяем средний элемент
        guess = list[mid]
        if guess == item:   #значение найдено
            return mid
        if guess > item:    #много
            high = mid - 1
        else:               #мало
            low = mid + 1
    return None             #значение не существует

my_list = [1, 3, 5, 7, 9, 11, 12, 17]
print(binary_search(my_list, 3))
print(binary_search(my_list, 12))
print(binary_search(my_list, 14))