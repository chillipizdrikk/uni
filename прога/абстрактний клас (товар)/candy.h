#pragma once
#include "product.h"

class Candy : public Product
{
private:
	std::string candyName;
	double candyWeight;
	double candyPrice; // per 1 kg

public:
	Candy();
	Candy(const std::string& maker, const std::string& name, double weight, double kgPrice);
	Candy(const Candy& C);
	virtual ~Candy();

	virtual void print() const override;
	virtual double getPrice() const override;
	virtual char getType() const override;
	virtual void readFrom(std::istream& in) override;
	virtual void writeTo(std::ostream& out) const override;
};