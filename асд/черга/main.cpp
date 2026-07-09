#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include <iostream>
#include "doctest.h"
using namespace std;


template <typename DataType>
struct Element {
    Element<DataType>* next; //вказівник на наступний елемент списку
    DataType value; //поле, що зберігає значення даних
    Element(DataType newValue) //новий об'єкт ініціалізує вказівник на наступне значення як нулптр
        : next(nullptr) {
        value = newValue;
    }
};

template <typename DataType>
class Queue { 
    Element<DataType>* head;
    Element<DataType>* tail;

public:
    Queue() 
        : head(nullptr), tail(nullptr) {
    }

    ~Queue() {
        while (!IsEmpty()) {
            Dequeue();
        }
    }

    bool IsEmpty() { //перевірка чи черга порожня
        bool result;
        result = head == nullptr;
        return result;
    }

    void Enqueue(DataType newValue) { //додавання нового елемента в кінець черги
        Element<DataType>* newElement = new Element<DataType>(newValue);
        if (!IsEmpty()) { // якщо черга не порожня, то додаємо новий елемент до хвоста і змінюємо вказівник на хвіст
            tail->next = newElement;
            tail = tail->next;
        }
        else { //якщо черга порожня, то встановлюємо вказівник на голову і хвіст
            head = newElement;
            tail = newElement;
        }
    }

    DataType Dequeue() { //видалення першого елемента черги
        if (IsEmpty()) {
            throw "Queue is empty!";
        }
        DataType result; //зберігаємо значення першого елемента черги
        result = head->value;
        Element<DataType>* deleteElement = head; //створюємо вказівник на елемент який треба видалити
        head = head->next; //змінюємо вказівник на голову
        delete deleteElement; //видаляємо перший елемент черги
        if (head == nullptr) { //якщо черга порожня, то вказівник на хвіст дорівнює нулптр
            tail = nullptr;
        }
        return result; //повертаємо значення першого елемента
    }

};

enum Priority {high = 0, normal = 1, low = 2}; //задаємо пріоритети за замовчуванням

template <typename DataType>
class PriorityQueue { //шаблон класу PriorityQueue, який реалізує пріоритетну чергу
    Queue<DataType> queues[low + 1];
public:
    void Enqueue(DataType value, Priority priority) { //метод для додавання елемента з заданим пріоритетом
        queues[priority].Enqueue(value);
    }

    DataType Dequeue() { //метод для вилучення елемента з найвищим пріоритетом
        Priority queueIndex = high;
        while (queueIndex <= low && queues[queueIndex].IsEmpty()) { //цикл шукає першу непорожню чергу
            queueIndex = (Priority)(queueIndex + 1);
        }

        return queues[queueIndex].Dequeue();  //вилучає елемент з першої непорожньої черги та повертає його
    }

    bool IsEmpty() { //метод для перевірки, чи є пріоритетна черга порожньою
        Priority queueIndex = high;
        while (queueIndex <= low && queues[queueIndex].IsEmpty()) { //цикл шукає першу непорожню чергу
            queueIndex = (Priority)(queueIndex + 1);
        }

        return queues[queueIndex].IsEmpty(); //повертає true, якщо вона порожня
    }
};


TEST_CASE("testing queue") {
    Queue<int> queue;
    CHECK(queue.IsEmpty() == true);
    queue.Enqueue(1);
    CHECK(queue.IsEmpty() == false);
    queue.Enqueue(2);
    queue.Enqueue(3);
    CHECK(queue.IsEmpty() == false);
    CHECK(queue.Dequeue() == 1);
    CHECK(queue.IsEmpty() == false);
    CHECK(queue.Dequeue() == 2);
    CHECK(queue.Dequeue() == 3);
    CHECK(queue.IsEmpty() == true);
}

TEST_CASE("testing queue(char)") {
    PriorityQueue<char> queue;

    queue.Enqueue('m', normal);
    queue.Enqueue('a', low);
    queue.Enqueue('r', high);
    queue.Enqueue('t', normal);
    CHECK(queue.Dequeue() == 'r');
    CHECK(queue.Dequeue() == 'm');
    CHECK(queue.Dequeue() == 't');
    CHECK(queue.Dequeue() == 'a');
}

TEST_CASE("testing queue(string)") {
    PriorityQueue<string> queue;

    queue.Enqueue("banana", normal);
    queue.Enqueue("orange", low);
    queue.Enqueue("lemon", high);
    queue.Enqueue("apple", normal);
    CHECK(queue.Dequeue() == "lemon");
    CHECK(queue.Dequeue() == "banana");
    CHECK(queue.Dequeue() == "apple");
    CHECK(queue.Dequeue() == "orange");
}