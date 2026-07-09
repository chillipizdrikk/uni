#include <iostream>
#include "ticket.h"
#include "business.h"

using namespace std;

int main()
{
    Ticket T1("Warsaw", 485, 25);
    Ticket T2("Berlin", 924.1, 40);
    Ticket T3("Brussel", 1615.8, 60);
    Ticket T4("Paris", 1863.6, 85);
  
    BusinessTicket B1("Valencia", 2913.3, 103, 20);
    BusinessTicket B2("Lisbon", 3560.3, 115, 13);
  
    Ticket* tickets[6];
    tickets[0] = &T1;
    tickets[1] = &B1;
    tickets[2] = &T2;
    tickets[3] = &T3;
    tickets[4] = &B2;
    tickets[5] = &T4;

    for (int i = 0; i < 6; i++) {
        tickets[i]->print();
    }

    double total = 0;
    for (int i = 0; i < 6; i++) {
        total += tickets[i]->totalPrice();
    }

    cout << "\nTOTAL COST: " << total << " uah.\n\n";

	return 0;
}