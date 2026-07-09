from protected_stack import ProtectedStack

def sum_nested(tree):
    stack = ProtectedStack()
    stack.push(tree)
    total = 0
    while not stack.is_empty():
        item = stack.pop()
        if isinstance(item, list):
            for el in item:
                stack.push(el)
        elif isinstance(item, int) or isinstance(item, float):
            total += item
        else:
            raise TypeError("Знайдено нечисловий елемент: %s" % repr(item))
    return total

def run_tests():
    test_cases = [
        ([5, 1, [3, [2, 2]], 6, [[4, [7, 7], [3,3,3]]]], 5+1+3+2+2+6+4+7+7+3+3+3),
        ([], 0),
        ([1], 1),
        ([[], [[], []]], 0),
        ([1, [2, [3, [4]]]], 1+2+3+4),
        ([1, [2, "a"]], "error"),
    ]
    test_case_index = 5
    input_tree, expected = test_cases[test_case_index]
    print(f"Тест {test_case_index}: {input_tree}")
    try:
        result = sum_nested(input_tree)
        print("Сума:", result)
        if expected == "error":
            print("Мала бути помилка!")
        else:
            assert result == expected
            print("Тест пройдено успішно.")
    except Exception as e:
        print("Помилка:", e)
        if expected != "error":
            print("Мала бути сума, а не помилка!")

if __name__ == "__main__":
    run_tests()