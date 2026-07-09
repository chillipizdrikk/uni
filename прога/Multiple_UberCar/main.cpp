#include <iostream>
#include "car.h"
#include "driver.h"
#include "uber_car.h"
using taxi::Car;
using taxi::Driver;
using taxi::UberCar;
using namespace std;

int main()
{
	Car audi;
	Car seat("Seat", 2500);
	audi.PrintCarInfo();
	seat.PrintCarInfo();
	cout << "\n";

	Driver test;
	Driver ivan("Ivan", 35);
	test.PrintDriverInfo();
	ivan.PrintDriverInfo();
	cout << "\n";

	UberCar taxi_ivan("Kyiv", seat, ivan);
	UberCar taxi_maria("Ternopil", "Fiat", 700, "Maria", 51);
	taxi_ivan.PrintUberInfo();
	taxi_ivan.PrintDriverInfo();
	cout << "\n";
	taxi_maria.PrintUberInfo();
	cout << "Taxi " << taxi_maria.get_driver_name();
	cout << " (" << taxi_maria.get_car_brand() << ")\n\n";

	cout << "---Uber as driver---\n";
	Driver* maria_ptr = &taxi_maria;
	maria_ptr->PrintDriverInfo();

	cout << "\n---Uber as car---\n";
	Car* fiat_ptr = &taxi_maria;
	fiat_ptr->PrintCarInfo();
	cout << "\n\n";

	return 0;
}