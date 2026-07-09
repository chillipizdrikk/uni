#include "ticket.h"
#include <iostream>

Ticket::Ticket(int seat, double price) 
    : seat(seat), price(price) {}

Ticket::~Ticket() {}

double Ticket::getPrice() const {
    return price;
}

void Ticket::printInfo() const {
    std::cout << "Seat number: " << seat << "\n";
    std::cout << "Ticket price: " << price << "\n";
} 

bool Ticket::operator<(const Ticket& t) const {
    return getPrice() < t.getPrice();
}

void Ticket::ReadFrom(std::istream& in) {
    in >> seat >> price;
}

void Ticket::WriteTo(std::ostream& out) const
{
    out << "Ticket: " << seat << ' ' << price << " uah\n";
}

std::istream& operator>>(std::istream& in, Ticket& t) {
    t.ReadFrom(in);
    return in;
}
std::ostream& operator<<(std::ostream& out, const Ticket& t) {
    t.WriteTo(out);
    return out;
}
