#include "itemsale.h"
using namespace std;

ItemSale::ItemSale()
	: Item()
	, saleValue(0)
{
	cout << "ItemSale - Default\n";
}

ItemSale::ItemSale(const std::string& name, double price, unsigned count, unsigned sale)
	: Item(name, price, count)
	, saleValue(sale)
{
	cout << "ItemSale - Parameter\n";
}

ItemSale::ItemSale(const ItemSale& S)
	: Item(S)
	, saleValue(S.saleValue)
{
	cout << "ItemSale - Copy\n";
}

ItemSale::~ItemSale()
{
	cout << "~ItemSale\n";
}

void ItemSale::print() const
{
	cout << "SALE " << saleValue << " %\n";
	Item::print();
}

double ItemSale::totalPrice() const
{
	double price = Item::totalPrice();
	double sale = price * (double)saleValue / 100.0;
	return price - sale;
}

void ItemSale::readFrom(std::istream& in)
{
	Item::readFrom(in);
	in >> saleValue;
}

void ItemSale::writeTo(std::ostream& out) const
{
	Item::writeTo(out);
	out << ' ' << saleValue;
}