class ProtectedStack:
    """Захищений стек (тільки через push/pop/peek, приватне зберігання)"""
    def __init__(self):
        self.__data = []

    def push(self, value):
        self.__data.append(value)

    def pop(self):
        if not self.__data:
            raise IndexError("Pop from empty stack")
        return self.__data.pop()

    def peek(self):
        if not self.__data:
            raise IndexError("Peek from empty stack")
        return self.__data[-1]

    def is_empty(self):
        return not self.__data

    def size(self):
        return len(self.__data)

    def __str__(self):
        return f"Stack({self.size()} elements)"