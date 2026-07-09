#pragma once
#include <iostream>

class Ticket {
protected:
    int seat;
    double price;

public:
    Ticket(int seat, double price);
    virtual ~Ticket();

    virtual double getPrice() const;
    virtual void printInfo() const;

    void ReadFrom(std::istream& in);
    void WriteTo(std::ostream& out) const;

    bool operator<(const Ticket& t) const;
};

std::istream& operator>>(std::istream& in, Ticket& t);
std::ostream& operator<<(std::ostream& out, const Ticket& t);