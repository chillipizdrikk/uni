#include <iostream>
#include <cstring>
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include"doctest.h"

using namespace std;

const int TABLE_SIZE = 128; //максимальний розмір хеш-таблиці взаємно простий з k інтервалом
//Фактор заповнення = (100 * (1 - (весь простір / весь простір з інформацією)))
class HashBucket { //вузол у хеш-таблиці
public:
    string key;
    string value;
    HashBucket* next;

    HashBucket(string k, string v) {
        key = k;
        value = v;
        next = nullptr;
    }

    ~HashBucket() {}
};

class HashTable {
private:
    HashBucket** table;//вказівник на масив вказівників на об'єкти HashBucket

public:
    HashTable() {
        table = new HashBucket * [TABLE_SIZE];
        for (int i = 0; i < TABLE_SIZE; i++)
            table[i] = nullptr;
    }

    ~HashTable() { //видалення всіх вузлів
        for (int i = 0; i < TABLE_SIZE; i++) {
            HashBucket* entry = table[i];
            while (entry != nullptr) {
                HashBucket* prev = entry;
                entry = entry->next;
                delete prev;
            }
        }
        delete[] table;
    }

    int hashFunc(const string& key) { //обчислює хеш-значення для заданого ключа
        int hashVal = 0;
        for (int i = 0; i < key.length(); i++)
            hashVal = 37 * hashVal + key[i]; //хеш-функція для рядків, використовуючи 37 як просте число
        hashVal %= TABLE_SIZE;//зменшує хеш-значення до розміру таблиці
        if (hashVal < 0)
            hashVal += TABLE_SIZE; //якщо значення від'ємне - коригуємо, додаючи до значення розмір таблиці
        return hashVal;
    }

    void insert(const string& key, const string& value) { //вставляє пару ключ-значення до хеш-таблиці
        int hashVal = hashFunc(key);//обчислює хеш-значення
        HashBucket* prev = nullptr;
        HashBucket* entry = table[hashVal];
        while (entry != nullptr && entry->key != key) { //перевіряє чи поточний вузол !=0 і поточний ключ !=заданому 
            prev = entry;
            entry = entry->next;
        }
        if (entry == nullptr) {
            entry = new HashBucket(key, value); //створюємо новий об'єкт з заданим ключем і значенням 
            if (prev == nullptr) //список порожній тому новий стає головою списку
                table[hashVal] = entry; 
            else //новий вузол вставляється після попереднього
                prev->next = entry;
        }
        else {
            entry->value = value;//ключ вже є в таблиці, значення вузла оновлюємо на нове
        }
    }

    string get(const string& key) { //отримує значення, пов'язане з заданим ключем у хеш-таблиці
        int hashVal = hashFunc(key); //обчислює хеш-значення
        HashBucket* entry = table[hashVal];
        while (entry != nullptr && entry->key != key)
            entry = entry->next;
        if (entry == nullptr) //ключ не знайдений у хеш - таблиці
            return "Key not found";
        else //ключ знайдений у хеш-таблиці, функція повертає значення, що зберігається у вузлі
            return entry->value; 
    }


    void remove(const string& key) { //видаляє пару ключ-значення з хеш-таблиці за заданим ключем
        int hashVal = hashFunc(key);//обчислює хеш-значення
        HashBucket* prev = nullptr;
        HashBucket* entry = table[hashVal];
        while (entry != nullptr && entry->key != key) {
            prev = entry;
            entry = entry->next;
        }
        if (entry == nullptr) //ключ не знайдений - видаляти не треба
            return;
        else {
            if (prev == nullptr)  //знайдений вузол є першим у зв'язаному списку тому переходимо на наступний
                table[hashVal] = entry->next;
            else //переходимо на наступний вузол
                prev->next = entry->next;
            delete entry;
        }
    }
};

TEST_CASE("Insert and get value") {
    HashTable t;
    t.insert("apple", "red");
    CHECK(t.get("apple") == "red");
}
TEST_CASE("Insert and get multiple values") {
    HashTable t;
    t.insert("banana", "yellow");
    t.insert("cherry", "red");
    CHECK(t.get("banana") == "yellow");
    CHECK(t.get("cherry") == "red");
}
TEST_CASE("Test hash function") {
    HashTable t;

    CHECK(t.hashFunc("apple") == 114);
    CHECK(t.hashFunc("banana") == 81);
    CHECK(t.hashFunc("cherry") == 13);
}
TEST_CASE("Update value of an existing key") {
    HashTable t;
    t.insert("apple", "green");
    CHECK(t.get("apple") == "green");
}
TEST_CASE("Remove") {
    HashTable t;
    t.remove("banana");
}