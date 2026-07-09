from protected_stack import ProtectedStack

def eval_formula(expr):
    stack = ProtectedStack()
    tokens = []
    i = 0
    n = len(expr)
    while i < n:
        ch = expr[i]
        if ch.isdigit():
            tokens.append(int(ch))
            i += 1
        elif expr.startswith("S(", i):
            tokens.append("S")
            i += 2
        elif expr.startswith("D(", i):
            tokens.append("D")
            i += 2
        elif ch == ',':
            tokens.append(",")
            i += 1
        elif ch == ')':
            tokens.append(")")
            i += 1
        elif ch.isspace():
            i += 1
        else:
            raise ValueError(f"Недопустимий символ: {ch}")
    value_stack = ProtectedStack()
    op_stack = ProtectedStack()
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if isinstance(tok, int):
            value_stack.push(tok)
            i += 1
        elif tok in ("S", "D"):
            op_stack.push(tok)
            i += 1
        elif tok == ",":
            i += 1
        elif tok == ")":
            arg2 = value_stack.pop()
            arg1 = value_stack.pop()
            op = op_stack.pop()
            if op == "S":
                value_stack.push(arg1 + arg2)
            else:
                if arg2 == 0:
                    raise ZeroDivisionError("Ділення на 0")
                value_stack.push(arg1 // arg2)
            i += 1
        else:
            raise ValueError(f"Недопустимий токен: {tok}")
    return value_stack.pop()

def run_tests():
    test_cases = [
        ("D(8,S(2,1))", 2),
        ("S(1,2)", 3),
        ("S(1,D(8,2))", 5),
        ("D(D(8,2),2)", 2),
        ("S(9,0)", 9),
        ("D(8,0)", "error"),
    ]
    test_case_index = 4
    input_expr, expected = test_cases[test_case_index]
    print(f"Тест {test_case_index}: '{input_expr}'")
    try:
        result = eval_formula(input_expr)
        print("Значення:", result)
        if expected == "error":
            print("Має бути помилка (ділення на 0)")
        else:
            assert result == expected
            print("Тест пройдено успішно.")
    except Exception as e:
        print("Помилка:", e)
        if expected != "error":
            print("Мала бути відповідь, а не помилка!")

if __name__ == "__main__":
    run_tests()