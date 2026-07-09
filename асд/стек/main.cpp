#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest.h"
#include <iostream>
using namespace std;

// максимальний розмір стеку
const int MAX_SIZE = 100;

class Stack {
private:
    // визначення змінних для зберігання елементів стеку у масиві та вказівника на вершину стеку
    int top;
    int arr[MAX_SIZE];
public:
    Stack() {
        top = -1;
    }

    // функція для додавання елемента в стек
    void Push(int val) {
        if (top >= MAX_SIZE - 1) {
            cout << "Stack overflow" << endl;
        }
        else {
            top++;
            arr[top] = val;
        }
    }

    // функція для видалення елемента зі стеку
    void Pop() {
        if (top <= -1) {
            cout << "Stack underflow" << endl;
        }
        else {
            top--;
        }
    }

    // функція для повернення значення елемента на вершині стеку, без його видалення
    int Peek() {
        if (top <= -1) {
            cout << "Stack is empty" << endl;
            return -1;
        }
        else {
            return arr[top];
        }
    }

    // функція, що повертає істину, якщо стек порожній
    bool IsEmpty() {
        return (top <= -1);
    }
};

TEST_CASE("Test 1") {
    Stack st;
    CHECK(st.IsEmpty() == true);
    st.Push(1);
    CHECK(st.IsEmpty() == false);
    st.Pop();
    CHECK(st.IsEmpty() == true);
}

TEST_CASE("Test 2") {
    Stack st;
    CHECK(st.IsEmpty() == true);
    st.Push(5);
    st.Push(10);
    CHECK(st.IsEmpty() == false);
    CHECK(st.Peek() == 10);
    st.Pop();
    CHECK(st.Peek() == 5);
    st.Pop();
    CHECK(st.IsEmpty() == true);
}

TEST_CASE("Test 3") {
    Stack st;
    st.Push(2);
    st.Push(4);
    st.Push(6);
    CHECK(st.IsEmpty() == false);
    CHECK(st.Peek() == 6);
    st.Pop();
    st.Pop();
    CHECK(st.IsEmpty() == false);
    CHECK(st.Peek() == 2);
    st.Pop();
    CHECK(st.IsEmpty() == true);
}