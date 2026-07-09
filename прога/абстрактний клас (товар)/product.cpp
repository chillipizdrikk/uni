#include "product.h"
#include "candy.h"
#include "device.h"
#include <fstream>
using namespace std;


Product::Product()
    :productMaker("")
{}

Product::Product(const string& maker)
    : productMaker(maker)
{}

Product::Product(const Product& P)
    : productMaker(P.productMaker)
{}

Product::~Product()
{}

void Product::print() const
{
    cout << "Manufacturer: " << productMaker;
}

void Product::readFrom(istream& in)
{
    in >> productMaker;
}

void Product::writeTo(ostream& out) const
{
    out << productMaker;
}

string Product::getManufacturer() const
{
    return productMaker;
}

bool Product::operator<(const Product& P) const
{
    return getPrice() < P.getPrice();
}

istream& operator>> (istream& in, Product& P)
{
    P.readFrom(in);
    return in;
}

ostream& operator<< (ostream& out, const Product& P)
{
    P.writeTo(out);
    return out;
}

size_t readProductsFromFile(Product**& arr, size_t& n, const std::string& fileName)
{
    ifstream iFile(fileName);
    iFile >> n;
    arr = new Product * [n];
    char type;
    size_t counter = 0;
    for (size_t i = 0; i < n; ++i)
    {
        iFile >> type;
        if (type == 'C')
        {
            arr[counter] = new Candy();
            iFile >> *arr[counter];
            ++counter;
        }
        else if (type == 'D')
        {
            arr[counter] = new Device();
            iFile >> *arr[counter];
            ++counter;
        }
        else
        {
            char temp[256];
            iFile.getline(temp, 256);
        }
    }



    iFile.close();
    return counter;
}
void printProductsArray(Product**& arr, size_t n)
{
    cout << "Collection of all products\n";
    for (size_t i = 0; i < n; ++i)
    {
        arr[i]->print();
    }
    cout << "\n";
}