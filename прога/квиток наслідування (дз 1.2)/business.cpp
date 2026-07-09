#include "business.h"
using namespace std;

BusinessTicket::BusinessTicket()
	:Ticket(), percentageValue(0)
{}


BusinessTicket::BusinessTicket(const std::string& name, double distance, double price, unsigned percentage)
	: Ticket(name, distance, price), percentageValue(percentage)
{}


BusinessTicket::BusinessTicket(const BusinessTicket& T)
:Ticket(T), percentageValue(T.percentageValue)
{}


BusinessTicket::~BusinessTicket()
{}


void BusinessTicket::print() const 
 {
	cout << "Percentage of increase value: " << percentageValue << " %\n";
	Ticket::print();
 }


double BusinessTicket::totalPrice() const
{
	double price = Ticket::totalPrice();
	double percentage = price * (double)percentageValue / 100.0;
	return price - percentage;
}


void BusinessTicket::readFrom(std::istream& in)
{
	Ticket::readFrom(in);
	in >> percentageValue;
}


void BusinessTicket::writeTo(std::ostream& out) const
{
	Ticket::writeTo(out);
	out << ' ' << percentageValue;
}