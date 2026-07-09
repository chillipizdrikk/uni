#include <iostream>
#include <fstream>
#include <cmath>
#include "car.h"
using namespace std;

class ValueException
{
private:
    double value;

public:
    ValueException(double val): value(val){}
    void prinInfo() const
    {
        cout << "ERROR: Value " << value << " is not valid!\n";
    }
};

double calculateSqrt(double val)
{
    /*if (val < 0)
        throw "ERROR: Value can not be negative!";*/

    if (val < 0)
        throw ValueException(val);
    if (val == 0)
        cout << "Zero not accepted!";
    return sqrt(val);
}

int main()
{
   /* double a;
    cout << "Enter double: "; cin >> a;

    try
    {
        double b = calculateSqrt(a);
        cout << "Sqrt(" << a << "): " << b << "\n\n";
    }
    catch (const char* err)
    {
        cout << err << "\n";
    }
    catch (const ValueException& V)
    {
        V.prinInfo();
    }
    catch (...)
    {
        cout << "Epic fail...\n";
    }*/

    ifstream iFile("info.txt");
    size_t n; iFile >> n;
    Car* pool = new Car[n];
    for (size_t i = 0; i < n; ++i)
    {
        iFile >> pool[i];
    }
    iFile.close();

    cout << "Cars pool\n";
    printCarsArray(pool, n);

    cout << "\nModify car pool\n";
    for (size_t i = 0; i < n; ++i)
    {
        cout << "Car #" << i + 1 << ": " << pool[i] << "\n";

        try
        {
            string brand; cout << "New brand: "; cin >> brand;
            pool[i].setBrand(brand);
            cout << "Brand updated to: " << pool[i].getBrand() << "\n";
        }
        catch (const BrandException& B)
        {
            B.printBrandError();
        }

        try
        {
            double price; cout << "New price: "; cin >> price;
            pool[i].setPrice(price);
            cout << "Price updated to: " << pool[i].getPrice() << "uah\n";
        }
        catch (const PriceException& P)
        {
            P.printPriceError();
        }
        cout << "\n";
    }

    cout << "\nUpdated cars pool\n";
    printCarsArray(pool, n);



    delete[] pool;
    return 0;
}