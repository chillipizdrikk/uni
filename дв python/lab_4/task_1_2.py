from protected_stack import ProtectedStack

def find_bracket_pairs_sorted_by_open(text):
    stack = ProtectedStack()
    pairs = []
    for i, ch in enumerate(text):
        if ch == '(':
            stack.push(i)
        elif ch == ')':
            open_idx = stack.pop()
            pairs.append((open_idx, i))
    if not stack.is_empty():
        raise ValueError("Надлишкові відкриваючі дужки")
    # просте сортування вручну
    result = []
    pairs_copy = pairs[:]
    while pairs_copy:
        min_pair = pairs_copy[0]
        for p in pairs_copy:
            if p[0] < min_pair[0]:
                min_pair = p
        result.append(min_pair)
        pairs_copy.remove(min_pair)
    return result

def run_tests():
    test_cases = [
        ("(a + (b) + ((c)))", [(0,14),(5,7),(9,13)]),
        ("x + (y) + (z)", [(4,6),(9,11)]),
        ("(((())))", [(0,7),(1,6),(2,5),(3,4)]),
        ("no brackets", []),
    ]
    test_case_index = 2
    input_text, expected = test_cases[test_case_index]
    print(f"Тест {test_case_index}: '{input_text}'")
    try:
        result = find_bracket_pairs_sorted_by_open(input_text)
        print("Пари дужок (відкрита по зростанню):", result)
        assert result == expected
        print("Тест пройдено успішно.")
    except Exception as e:
        print("Помилка:", e)

if __name__ == "__main__":
    run_tests()