#pragma once
#include <string>
#include <iostream>

class Ticket
{
protected:
	std::string cityDestination;
	double cityDistance;
	double ticketPrice;

public:
	Ticket();
	Ticket(const std::string& name, double distance, double price);
	Ticket(const Ticket& T);
	virtual ~Ticket();

	virtual void print() const;
	virtual double totalPrice() const;
	virtual void readFrom(std::istream& in);
	virtual void writeTo(std::ostream& out) const;

	void increasePrice(double increase);
	bool operator < (const Ticket& T) const;

};

std::istream& operator >>(std::istream& in, Ticket& T);
std::ostream& operator <<(std::ostream& out, const Ticket& T);
