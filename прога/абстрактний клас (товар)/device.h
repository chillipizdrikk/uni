#pragma once
#include "product.h"

class Device : public Product
{
private:
	std::string deviceName;
	double devicePrice;

public:
	Device();
	Device(const std::string& maker, const std::string& name, double price);
	Device(const Device& D);
	virtual ~Device();

	virtual void print() const override;
	virtual double getPrice() const override;
	virtual char getType() const override;
	virtual void readFrom(std::istream& in) override;
	virtual void writeTo(std::ostream& out) const override;
};
