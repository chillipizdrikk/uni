#pragma once
#include "ticket.h"

class VIPTicket : public Ticket {
private:
    double popcornWeight;

public:
    VIPTicket(int seat, double price, double weight)
        : Ticket(seat, price), popcornWeight(weight) {}

    void printInfo() const {
        Ticket::printInfo();
        std::cout << "Popcorn weight: " << popcornWeight << " gr" << "\n";
    }

};


