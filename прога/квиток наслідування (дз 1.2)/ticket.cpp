#include "ticket.h"
using namespace std;

Ticket::Ticket()
    : cityDestination(""), cityDistance(0.0), ticketPrice(0.0)
{}


Ticket::Ticket(const std::string& name, double distance, double price)
    : cityDestination(name), cityDistance(distance), ticketPrice(price)
{}


Ticket::Ticket(const Ticket& T)
    :cityDestination(T.cityDestination), cityDistance(T.cityDistance), ticketPrice(T.ticketPrice)
{}


Ticket::~Ticket()
{}


void Ticket::print() const
{
    cout << "Destination: " << cityDestination << "\n";
    cout << "Distance: " << cityDistance << " km.\n";
    cout << "Ticket price: " << ticketPrice << " uah.\n";
    cout << "Total price: " << totalPrice() << " uah.\n\n";
}


double Ticket::totalPrice() const
{
    return cityDistance * ticketPrice;
}


void Ticket::readFrom(std::istream& in)
{
    in >> cityDestination >> cityDistance >> ticketPrice;
}


void Ticket::writeTo(std::ostream& out) const
{
    out << cityDestination << ' ' << cityDistance << ' ' << ticketPrice;
}


void Ticket::increasePrice(double increase)
{
    ticketPrice += increase;
}


bool Ticket::operator < (const Ticket& T) const
{
    return totalPrice() < T.totalPrice();
}


std::istream& operator >>(std::istream& in, Ticket& T)
{
    T.readFrom(in);
    return in;
}
 

std::ostream& operator <<(std::ostream& out, const Ticket& T)
{
  T.writeTo(out);
  return out;
}
