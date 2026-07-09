#pragma once
#include <string>
#include <iostream>

class Item
{
protected:
	std::string itemName;
	double itemPrice;
	unsigned itemCount;

public:
	Item();
	Item(const std::string& name, double price, unsigned count);
	Item(const Item& I);
	virtual ~Item();

	virtual void print() const;
	virtual double totalPrice() const;
	virtual void readFrom(std::istream& in);
	virtual void writeTo(std::ostream& out) const;

	void increaseCount(unsigned increase);
	bool operator < (const Item& I) const;

};

std::istream& operator >>(std::istream& in, Item& I);
std::ostream& operator <<(std::ostream& out, const Item& I);

void printProducts(Item** arr, size_t n);
void sortProducts(Item** arr, size_t n);