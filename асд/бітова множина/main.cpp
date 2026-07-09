#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest.h"
#include <iostream>
using namespace std;

class BitSet {
    int set[8] = { 0 }; //масив для зберігання бітового представлення множини
public:
    void Add(char new_element) { //додає новий елемент до множини
        int bitmask;
        bitmask = 1 << (new_element % 32); //зсув 1 на позицію нового елемента
        set[new_element / 32] = set[new_element / 32] | bitmask; //додаємо новий елемент до множини за допомогою побітового "або"
    }

    void Remove(char element) { //видаляє елемент з множини
        int bitmask;
        bitmask = 1 << (element % 32);
        set[element / 32] = set[element / 32] & (~bitmask); //видаляємо елемент з множини за допомогою побітового "і" з запереченням маски
    }

    bool IsInSet(char element) { //перевіряє, чи присутній елемент у множині за допомогою побітового "і"
        int bitmask;
        bitmask = 1 << (element % 32);
        return set[element / 32] & bitmask;
    }

    BitSet Intersect(BitSet other) { //перетин двох множин за допомогою побітового "і"
        BitSet result;
        for (int i = 0; i < 8; i++) {
            result.set[i] = this->set[i] & other.set[i];
        }
        return result;
    }

    BitSet Union(BitSet other) { //об'єднання двох множин за допомогою побітового "або"
        BitSet result;
        for (int i = 0; i < 8; i++) {
            result.set[i] = this->set[i] | other.set[i];
        }
        return result;
    }
};

TEST_CASE("Add element to BitSet and check if it is in set") {
    BitSet bitSet;
    bitSet.Add(1);
    CHECK(bitSet.IsInSet(1) == true);
}

TEST_CASE("Remove element from BitSet and check if it is not in set") {
    BitSet bitSet;
    bitSet.Add(1);
    bitSet.Remove(1);
    CHECK(bitSet.IsInSet(1) == false);
}

TEST_CASE("Intersect two BitSets and check if the result is correct") {
    BitSet bitSet1, bitSet2, expectedBitSet;
    bitSet1.Add(1);
    bitSet1.Add(2);
    bitSet1.Add(3);
    bitSet2.Add(2);
    bitSet2.Add(3);
    bitSet2.Add(4);
    expectedBitSet.Add(2);
    expectedBitSet.Add(3);
    BitSet resultBitSet = bitSet1.Intersect(bitSet2);
    CHECK(resultBitSet.IsInSet(1) == false);
    CHECK(resultBitSet.IsInSet(2) == true);
    CHECK(resultBitSet.IsInSet(3) == true);
    CHECK(resultBitSet.IsInSet(4) == false);
}

TEST_CASE("Union two BitSets and check if the result is correct") {
    BitSet bitSet1, bitSet2, expectedBitSet;
    bitSet1.Add(1);
    bitSet1.Add(2);
    bitSet2.Add(2);
    bitSet2.Add(3);
    expectedBitSet.Add(1);
    expectedBitSet.Add(2);
    expectedBitSet.Add(3);
    BitSet resultBitSet = bitSet1.Union(bitSet2);
    CHECK(resultBitSet.IsInSet(1) == true);
    CHECK(resultBitSet.IsInSet(2) == true);
    CHECK(resultBitSet.IsInSet(3) == true);
    CHECK(resultBitSet.IsInSet(4) == false);
}
