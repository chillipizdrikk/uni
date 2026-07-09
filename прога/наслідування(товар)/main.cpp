#include <iostream>
#include <fstream>
#include "itemsale.h"
using namespace std;

int main()
{
    ifstream iFile("products.txt");
    size_t itemN; iFile >> itemN;
    Item* itemArr = new Item[itemN];
    for (size_t i = 0; i < itemN; ++i)
        iFile >> itemArr[i];
    iFile.close();
    
    iFile.open("sales.txt");
    size_t salesN; iFile >> salesN;
    ItemSale* saleArr = new ItemSale[salesN];
    for (size_t i = 0; i < salesN; ++i)
        iFile >> saleArr[i];
    iFile.close();

    cout << "Simple products\n";
    for (size_t i = 0; i < itemN; ++i)
    {
        itemArr[i].print(); cout << "\n";
    }
    cout << "\n\n";
    
    cout << "Sale products\n";
    for (size_t i = 0; i < salesN; ++i)
    {
        saleArr[i].print(); cout << "\n";
    }
    cout << "\n\n";

    size_t n = itemN + salesN;
    Item** silpo = new Item * [n];
    size_t index = 0;
    for (size_t i = 0; i < itemN; ++i, ++index)
        silpo[index] = &itemArr[i];
    for (size_t i = 0; i < salesN; ++i, ++index)
        silpo[index] = &saleArr[i];

    cout << "Silpo products\n";
    sortProducts(silpo, n);
    printProducts(silpo, n);

	

  
    delete[] itemArr;
    delete[] saleArr;
    delete[] silpo;

	return 0;
}

/*Item A;
    Item B("Chocolate", 30.5, 2);
    Item C(B);

    A.print(); cout << "\n";
    B.print(); cout << "\n";
    C.print(); cout << "\n";*/

    /*ItemSale A; cout << "\n";
      ItemSale B("Chocolate", 30.5, 2, 10); cout << "\n";
      ItemSale C(B); cout << "\n\n";

      A.print(); cout << "\n";
      B.print(); cout << "\n";
      C.print(); cout << "\n\n";*/