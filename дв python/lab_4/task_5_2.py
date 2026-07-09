from protected_stack import ProtectedStack

def sort_stack(initial):
    """Сортує стек за допомогою двох додаткових стеків (без рекурсії, лише push/pop/peek/is_empty/size)"""
    src = ProtectedStack()
    for el in initial[::-1]: # спочатку на стек верхній елемент — останній у списку
        src.push(el)
    aux = ProtectedStack()
    dest = ProtectedStack()
    while not src.is_empty():
        temp = src.pop()
        while not dest.is_empty() and dest.peek() > temp:
            aux.push(dest.pop())
        dest.push(temp)
        while not aux.is_empty():
            dest.push(aux.pop())
    result = []
    while not dest.is_empty():
        result.append(dest.pop())
    return result[::-1]

def run_tests():
    test_cases = [
        ([4,1,3,2], [1,2,3,4]),
        ([5,4,3,2,1], [1,2,3,4,5]),
        ([1,2,3,4,5], [1,2,3,4,5]),
        ([1,3,2], [1,2,3]),
        ([3], [3]),
        ([], []),
    ]
    test_case_index = 1
    input_stack, expected = test_cases[test_case_index]
    print(f"Тест {test_case_index}: {input_stack}")
    result = sort_stack(input_stack)
    print("Відсортовано:", result)
    assert result == expected, f"Очікувана відповідь: {expected}, отримано: {result}"
    print("Тест пройдено успішно.")

if __name__ == "__main__":
    run_tests()