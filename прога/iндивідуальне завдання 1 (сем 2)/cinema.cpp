#include "cinema.h"
#include <iostream>
#include <fstream>
#include <sstream>

Cinema::Cinema(const std::string& movie)
    : cinemaName(movie) {}

Cinema::Cinema(const Cinema& other) {
    cinemaName = other.cinemaName;
    for (const auto& ticket : other.tickets) {
        if (dynamic_cast<VIPTicket*>(ticket)) {
            tickets.push_back(new VIPTicket(*dynamic_cast<VIPTicket*>(ticket)));
        }
        else {
            tickets.push_back(new Ticket(*ticket));
        }
    }
}

Cinema::~Cinema() {
    for (auto& ticket : tickets) {
        delete ticket;
    }
}

void Cinema::addTicket(Ticket* ticket) {
    tickets.push_back(ticket);
}

void Cinema::printTickets() const {
    for (const auto& ticket : tickets) {
        ticket->printInfo();
        std::cout << "\n";
    }
}

Ticket* Cinema::operator[](int index) const {
    if (index >= 0 && index < tickets.size()) {
        return tickets[index];
    }
    return nullptr;
}

void Cinema::readFromFile(const std::string& filename) {
    std::ifstream file(filename);
    if (file.is_open()) {
        std::string line;
        while (std::getline(file, line)) {
            std::istringstream iss(line);
            char ticketType;
            int seatNumber;
            double price;
            double popcornWeight;
            if (iss >> ticketType >> seatNumber >> price >> popcornWeight) {
                if (ticketType == 'V') {
                    tickets.push_back(new VIPTicket(seatNumber, price, popcornWeight));
                }
                else {
                    tickets.push_back(new Ticket(seatNumber, price));
                }
            }
        }
        file.close();
    }
    else {
        std::cout << "Cannot open file: " << filename << "\n";
    }
}

double Cinema::getTotalOfTickets() const {
    double totalPrice = 0.0;
    for (const auto& ticket : tickets) {
        totalPrice += ticket->getPrice();
    }
    return totalPrice;
}

double Cinema::getTotalOfVIPTickets() const {
    double totalPrice = 0.0;
    for (const auto& ticket : tickets) {
        if (dynamic_cast<VIPTicket*>(ticket)) {
            totalPrice += ticket->getPrice();
        }
    }
    return totalPrice;
}

Ticket* Cinema::getMostExpensive() const {
    if (tickets.empty()) {
        return nullptr;
    }

    Ticket* mostExpensiveTicket = tickets[0];
    for (const auto& ticket : tickets) {
        if (ticket->operator<(*mostExpensiveTicket)) {
            mostExpensiveTicket = ticket;
        }
    }
    return mostExpensiveTicket;
}

VIPTicket* Cinema::getCheapestVIP() const {
    VIPTicket* cheapestVIPTicket = nullptr;
    for (const auto& ticket : tickets) {
        if (VIPTicket* vipTicket = dynamic_cast<VIPTicket*>(ticket)) {
            if (cheapestVIPTicket == nullptr || *vipTicket < *cheapestVIPTicket) {
                cheapestVIPTicket = vipTicket;
            }
        }
    }
    return cheapestVIPTicket;
}
