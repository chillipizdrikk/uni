from collections import Counter
from random import randint

#завдання 1
def same_digits(num):
    num_str = str(num)
    for i in range(len(num_str) - 1):
        if num_str[i] == num_str[i + 1]:
            if i >= 1 and num_str[i-1] == num_str[i]:
                return False
            if i+2 < len(num_str) and num_str[i+2] == num_str[i]:
                return False
            return True
    return False


N = int(input("Введіть число N: "))
numbers = [randint(1, 10000) for _ in range(N)]
two_digit_numbers = [num for num in numbers if 10 <= num < 100]
count = len(two_digit_numbers)
same_digit_numbers = [num for num in numbers if same_digits(num)]


print(f"Початковий список: {numbers}")
print(f"Кінцевий список: {same_digit_numbers}")
print(f"Кількість двоцифрових чисел: {count}")

print('\n\n\n')

#завдання 2
cookbook = {
    'Борщ': {
        'Буряк': 300,
        'Картопля': 200,
        'Морква': 100,
        'Цибуля': 100,
        'Капуста': 200
    },
    'Вареники': {
        'Борошно': 500,
        'Яйця': 100,
        'Олія': 30,
        'Картопля': 300,
        'Цибуля': 100
    },
    'Омлет': {
        'Яйця': 200,
        'Молоко': 50,
        'Помідор': 50,
        'Сіль': 5,
        'Масло': 20
    },
    'Карбонара': {
        'Спагеті': 200,
        'Бекон': 100,
        'Яйця': 50,
        'Сир Пармезан': 50
    },
    'Цезар': {
        'Курка': 200,
        'Салат': 100,
        'Сир Пармезан': 50,
        'Сухарі': 50
    }
}

for dish, ingredients in cookbook.items():
    print(f"\n\t---{dish}---")
    for ing, amount in ingredients.items():
        print(f"\t{ing} - {amount} г")

ing_count = Counter(ing for ingredients in cookbook.values() for ing in ingredients)

frequent_ing = ing_count.most_common(1)[0]
print(f"\nІнгредієнт, який найчастіше використовується: {frequent_ing[0]}")

input_ing = input("\nВведіть назву інгредієнта: ")

for dish, ingredients in cookbook.items():
    if input_ing in ingredients:
        print(f"Використовується у страві \"{dish}\", для неї потрібно {ingredients[input_ing]} г цього інгредієнта")