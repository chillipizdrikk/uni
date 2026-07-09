from protected_stack import ProtectedStack

def validate_formula(expr):
    stack = ProtectedStack()
    i = 0
    n = len(expr)
    bracket_pairs = {')':'(', ']':'[', '}':'{'}
    while i < n:
        ch = expr[i]
        if ch in '([{':
            stack.push(ch)
            i += 1
        elif ch in ')]}':
            if stack.is_empty():
                return False
            open_br = stack.pop()
            if bracket_pairs[ch] != open_br:
                return False
            i += 1
        elif ch in '+-':
            i += 1
        elif ch in 'xyz':
            i += 1
        elif ch.isspace():
            i += 1
        else:
            return False
    return stack.is_empty()

def run_tests():
    test_cases = [
        ("x + ( y - z - [ x + x ] + { [ z - z - y ] + ( y ) } ) - z", True),
        ("x + ( y - z - [ x + x ] + { [ z - z - y ] + ( y ) } ) - z )", False),
        ("x + [ y - z )", False),
        ("x + (y)", True),
        ("(x)", True),
        ("x", True),
        ("(", False),
        ("", True),
        ("x + )", False),
    ]
    test_case_index = 7
    input_formula, expected = test_cases[test_case_index]
    print(f"Тест {test_case_index}: '{input_formula}'")
    result = validate_formula(input_formula)
    print("Коректність формули:", result)
    assert result == expected, "Невірний результат!"
    print("Тест пройдено успішно.")

if __name__ == "__main__":
    run_tests()