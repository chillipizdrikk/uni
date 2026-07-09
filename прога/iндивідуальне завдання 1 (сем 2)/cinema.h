#pragma once
#include <string>
#include <vector>
#include "ticket.h"
#include "vip_ticket.h"

class Cinema {
private:
    std::string cinemaName;
    std::vector<Ticket*> tickets;

public:
    Cinema(const std::string& cinema);
    Cinema(const Cinema& other);
    ~Cinema();

    void addTicket(Ticket* ticket);
    void printTickets() const;
    void readFromFile(const std::string& filename);
    double getTotalOfTickets() const;
    double getTotalOfVIPTickets() const;

    Ticket* operator[](int index) const;
    Ticket* getMostExpensive() const;
    VIPTicket* getCheapestVIP() const;
};