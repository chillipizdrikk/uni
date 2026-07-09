#  - Дочірній процес для task3_wait_main.py
#  - Зчитує дані з файлу comdata.txt, множить кожен елемент на 2,
#    друкує отримані дані у консоль і записує назад у файл.
#  - Має print() перед/після операцій та наприкінці очікує Enter, щоб було видно вікно консольного процесу.

fn = "comdata.txt"  # спільний файл даних

print("task3_child.py - початок (дочірній процес)")
print("Читаю дані з файлу:", fn)
with open(fn, "r") as subdata:
    cd = [int(x) for x in subdata.readline().rstrip().split()]
print("Дані, прочитані дочірнім процесом:", cd)

# Модифікація: множимо кожен елемент на 2
for k in range(len(cd)):
    cd[k] *= 2
print("Дані після множення на 2:", cd)

# Запис назад у файл
with open(fn, "w") as subdata:
    subdata.write(" ".join(map(str, cd)) + "\n")
print("Дані записані назад у файл:", fn)

input("Дочірній процес: натисніть Enter щоб завершитись і повернути управління основному процесу...")
print("task3_child.py - кінець")