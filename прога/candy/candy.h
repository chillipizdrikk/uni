#pragma once
#include <iostream>
#include <string>
using namespace std;

class Candy
{
private:
	string candyName;
	double candyPrice;
	double candyWeight;
	double candyBoxPrice;

	void calculateCandyPrice();

public:
	Candy()
		:candyName("no name"), candyPrice(0), candyWeight(0) {}
	Candy(string name, double price, double weight)
		: candyName(name), candyPrice(price), candyWeight(weight) {}
	Candy(const Candy& C)
		: candyName(C.candyName), candyPrice(C.candyPrice), candyWeight(C.candyWeight) {}
	~Candy(){}

	string getName() const;
	double getPrice() const;
	double getWeight() const;
	double getBoxPrice() const;

	void setName(const string& name);
	void setPrice(double price);
	void setWeight(double weight);

	void readFromFile(istream& in);
	void writeIntoFile(ostream& out) const;
	void printCandy() const;
};

istream& operator>>(istream& in, Candy& C);
ostream& operator<<(ostream& out, const Candy& C);

void printCandyArray(const Candy* arr, size_t n);
