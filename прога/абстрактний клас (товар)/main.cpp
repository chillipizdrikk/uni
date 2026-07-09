#include <iostream>
#include "candy.h"
#include "device.h"
using namespace std;

int main()
{
    size_t nAll, n;
    Product** shop = nullptr;
    n = readProductsFromFile(shop, nAll, "goods.txt");
    printProductsArray(shop, n);

    size_t candyCount = 0;
    size_t deviceCount = 0;
    double totalPrice = 0;
    double candyPrice = 0;
    double devicePrice = 0;
    for (size_t i = 0; i < n; ++i)
    {
        totalPrice += shop[i]->getPrice();
        if (shop[i]->getType() == 'C')
        {
            ++candyCount;
            candyPrice += shop[i]->getPrice();
        }
        else
        {
            ++deviceCount;
            devicePrice += shop[i]->getPrice();
        }
    }
    cout << "Nof Candies: " << candyCount;
    cout << ". Total price: " << candyPrice << " uah\n";
    cout << "Nof Devices: " << deviceCount;
    cout << ". Total price: " << devicePrice << " uah\n";
    cout << "TOTAL: " << totalPrice << " UAH\n\n";



    // Delete shop !!!
    for (size_t i = 0; i < n; ++i)
        delete shop[i];
    delete[] shop;


    /*Candy C1 ("Svitoch", "Romashka", 0.75, 35.1);
    Product* C2 = new Candy("Roshen", "Mak", 0.9, 41.2);

    C1.print();
    C2->print();

    Device D1("Bosch", "Mixer", 350.0);



    delete[] C2;*/
    return 0;
}