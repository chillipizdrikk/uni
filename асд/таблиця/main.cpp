#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest.h"
#include <iostream>
#include <math.h>
#include <string>

using namespace std;

class Row {
public:
    string Surname;
    string Name;
    int Age = 0;

    Row() 
        :Age(0) {}

    Row(string surname, string name = "", int age = 0) 
        : Surname(surname), Name(name), Age(age) {}

    Row(const Row& from) {
        *this = from;
    }

    Row& operator=(const Row& other) {
        this->Surname = other.Surname;
        this->Age = other.Age;
        this->Name = other.Name;
        return *this;
    }

    bool EqualFields(const Row& other) { //перевіряє, чи рівні поля об'єкта 
        bool result;
        result = this->Surname == other.Surname && this->Name == other.Name && this->Age == other.Age;
        return result;
    }

    bool operator == (const Row& other) {
        bool result;
        result = this->Surname == other.Surname;
        return result;
    }

    bool operator < (const Row& other) {
        bool result;
        result = this->Surname < other.Surname;
        return result;
    }
};

class Node {
public:
    Node() {}
    Row val;
    Node* left = nullptr;
    Node* right = nullptr;
};

class Table {
    Node* root = nullptr;

    Node* Find(string surname, Node* start_search, Node*& parent) { // метод для пошуку вузла
        Node* result = nullptr;
        if (start_search != nullptr) { //перевіряємо, чи поточний вузол не є nullptr
            if (start_search->val.Surname == surname) { //дивимось чи поточний збігається з шуканим
                result = start_search;
            }
            else {
                parent = start_search;
                if (surname < start_search->val.Surname) {
                    //йдемо наліво                    
                    result = Find(surname, start_search->left, parent);
                }
                else {
                    //йдемо направо
                    result = Find(surname, start_search->right, parent);
                }

            }
        }
        return result;
    };

public:
    
    bool ReplaceRow(const Row& row) { //заміна значення рядка у таблиці
        bool result = false;
        Node* find;
        Node* parent;
        find = Find(row.Surname, root, parent); //пошук заданого прізвища
        if (find != nullptr) {
            result = true;
            find->val = row; //оновлене значення замінює попереднє
        }
        return result;
    }

    bool FindRow(Row& row) { //пошук рядка в таблиці за заданим прізвищем
        bool result = false;
        Node* find;
        Node* parent;
        find = Find(row.Surname, root, parent);
        if (find != nullptr) {
            result = true;
            row = find->val; //значення полів копіюються до row
        }
        return result;
    }

    bool IsKeyInTable(string surname) { //перевіряє наявність рядка з заданим прізвищем у таблиці
        Row row(surname);
        bool result = FindRow(row);
        return result;
    }
   
    bool AddRow(const Row& element) { //додає новий рядок до таблиці
        bool result = false;
        if (root == nullptr) //якшо таблиця порожня, то додаємо новий вузол
        {
            root = new Node();
            root->val = element;
            result = true;
        }
        else {
            Node* find;
            Node* parent;
            find = Find(element.Surname, root, parent); //пошук заданого прізвища
            if (find == nullptr) { //якщо прізвище не знайдено, то додаємо новий вузол
                Node* new_node = new Node();
                new_node->val = element;
                if (parent->val < element) { //якщо значення батьківського менше за поточне, то йдемо направо
                    parent->right = new_node;
                }
                else {
                    parent->left = new_node; //йдемо наліво
                }
            }
        }
        return result;
    }
};


TEST_CASE("Test 1") {
    Table t;
    CHECK(t.IsKeyInTable("Tryhub") == false);
    t.AddRow(Row("Tryhub"));
    CHECK(t.IsKeyInTable("Tryhub") == true);
    t.AddRow(Row("Dopko"));
    t.AddRow(Row("Bernikova"));
    t.AddRow(Row("Plesak"));
    CHECK(t.IsKeyInTable("Dopko") == true);
    CHECK(t.IsKeyInTable("Bernikova") == true);
    CHECK(t.IsKeyInTable("Plesak") == true);
}


TEST_CASE("Test 2") {
    Table t;
    Row correct("Tryhub", "Marta", 17);
    t.AddRow(correct);
    Row find_row("Tryhub");
    bool find_result = t.FindRow(find_row);
    CHECK(correct.EqualFields(find_row) == true);
    CHECK(find_result == true);
}

TEST_CASE("Test 3 (replace)") {
    Table t;

    Row modified("Tryhub", "Anna", 18);
    bool replace = t.ReplaceRow(modified);
    CHECK(replace == false);
    Row correct("Tryhub", "Marta", 17);
    t.AddRow(correct);

    replace = t.ReplaceRow(modified);
    CHECK(replace == true);

    Row find_row("Tryhub");
    bool find_result = t.FindRow(find_row);

    CHECK(modified.EqualFields(find_row) == true);
    CHECK(find_result == true);
}

