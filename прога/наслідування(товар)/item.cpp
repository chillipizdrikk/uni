#include "item.h"
using namespace std;


Item::Item()
    : itemName(""), itemPrice(0.0), itemCount(0)
{
    //cout << "Item - Default\n";
}



Item::Item(const std::string& name, double price, unsigned count)
    : itemName(name), itemPrice(price), itemCount(count)
{
    //cout << "Item - Parameter\n";
}



Item::Item(const Item& I)
    : itemName(I.itemName), itemPrice(I.itemPrice), itemCount(I.itemCount)
{
    //cout << "Item - Copy\n";
}



Item::~Item()
{
    //ñout << "~Item\n";
}



void Item::print() const
{
   cout << "Product: " << itemName << "\n";
   cout << "Price per unit: " << itemPrice << " uah. ";
   cout << "Total amount: " << itemCount << "\n";
   cout << "Total price: " << totalPrice() << "uah.\n";
}


double Item::totalPrice() const
{
    return itemPrice * (double)itemCount;
}

void Item::readFrom(istream& in)
{
    in >> itemName >> itemPrice >> itemCount;
}

void Item::writeTo(ostream& out) const
{
    out << itemName << ' ' << itemPrice << ' ' << itemCount;
}

void Item::increaseCount(unsigned increase)
{
    itemCount += increase;
}

bool Item::operator < (const Item& I) const
{
    return totalPrice() < I.totalPrice();
}

istream& operator >> (istream& in, Item& I)
{
    I.readFrom(in);
    return in;
}

ostream& operator << (ostream& out, const Item& I)
{
    I.writeTo(out);
    return out;
}

void printProducts(Item** arr, size_t n)
{
    for (size_t i = 0; i < n; ++i)
    {
        arr[i]->print(); cout << "\n";
    }
    cout << "\n\n";
}

void sortProducts(Item** arr, size_t n)
{
    for (size_t i = 0; i < n; ++i)
    {
        size_t M = i;
        for (size_t j = i + 1; j < n; ++j)
        {
            if (*arr[j] < *arr[M])
                M = j;
        }
        if (M != i)
        {
            Item* temp = arr[i];
            arr[i] = arr[M];
            arr[M] = temp;
        }
    }
}