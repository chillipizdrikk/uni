from protected_stack import ProtectedStack

def find_bracket_pairs(text):
    stack = ProtectedStack()
    pairs = []
    for i, ch in enumerate(text):
        if ch == '(':
            stack.push(i)
        elif ch == ')':
            if stack.is_empty():
                raise ValueError("Надлишкова закриваюча дужка на позиції %d" % i)
            open_idx = stack.pop()
            pairs.append((open_idx, i))
    if not stack.is_empty():
        raise ValueError("Надлишкові відкриваючі дужки")
    return pairs

def run_tests():
    test_cases = [
        ("(a + (b) + ((c)))", [(0,14),(5,7),(9,13)]),
        ("x + (y) + (z)", [(4,6),(9,11)]),
        ("(((())))", [(3,4),(2,5),(1,6),(0,7)]),
        ("no brackets", []),
        ("(()(()))", [(1,2),(4,5),(3,6),(0,7)]),
        ("(", "error"),
        (")", "error"),
        ("(())", [(0,3),(1,2)]),
    ]
    test_case_index = 3
    input_text, expected = test_cases[test_case_index]
    print(f"Тест {test_case_index}: рядок '{input_text}'")
    try:
        result = find_bracket_pairs(input_text)
        print("Пари дужок:", result)
        if expected == "error":
            print("Очікувалась помилка, але її не виникло!")
        else:
            assert sorted(result) == sorted(expected), f"Відповідь некоректна: {result} vs {expected}"
            print("Тест пройдено успішно.")
    except Exception as e:
        print("Отримано помилку:", e)
        if expected != "error":
            print("Помилка неочікувана!")

if __name__ == "__main__":
    run_tests()