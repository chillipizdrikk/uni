#pragma once
#include "item.h"

class ItemSale : public Item
{
private:
unsigned saleValue;

public:
	ItemSale();
	ItemSale(const std::string& name, double price, unsigned count, unsigned sale);
	ItemSale(const ItemSale& S);
	virtual ~ItemSale();
	
	virtual void print() const override;
	virtual double totalPrice() const override;
	virtual void readFrom(std::istream& in) override;
	virtual void writeTo(std::ostream& out) const override;
};