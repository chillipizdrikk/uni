#include "cinema.h"
#include <iostream>
#include <fstream>
using namespace std;

int main() {
    Cinema cinema("Movie name");
    cinema.addTicket(new Ticket(6, 100.5));
    cinema.addTicket(new VIPTicket(7, 155.5, 120.0)); 
    cinema.readFromFile("cinema.txt");
    cinema.printTickets();

    double totalPrice = cinema.getTotalOfTickets();
    double totalVIPPrice = cinema.getTotalOfVIPTickets();
    cout << "Total price of tickets: " << totalPrice << "\n";
    cout << "Total price of VIP tickets: " << totalVIPPrice << "\n\n";

    Ticket* mostExpensiveTicket = cinema.getMostExpensive();
    VIPTicket* cheapestVIPTicket = cinema.getCheapestVIP();
    cout << "---The most expensive ticket---" << "\n";
    if (mostExpensiveTicket != nullptr) {
        mostExpensiveTicket->printInfo();
    }
    else {
       cout << "There is no tickets" << "\n";
    }
    cout << "\n---The cheapest VIP ticket---" << "\n";
    if (cheapestVIPTicket != nullptr) {
        cheapestVIPTicket->printInfo();
    }
    else {
        cout << "There is no VIP tickets" << "\n";
    }

    return 0;
}
