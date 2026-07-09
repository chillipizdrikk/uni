#include "uber_car.h"
#include <iostream>
using std::cout;
using std::string;

namespace taxi {
	UberCar::UberCar()
		: Car(), Driver(), uber_city_("Lviv") {
	}

	UberCar::UberCar(const std::string& city, const std::string& brand, double price, const std::string& name, unsigned age)
		: Car(brand, price), Driver(name, age), uber_city_(city) {
	}

	UberCar::UberCar(const std::string& city, const Car& c, const Driver& d)
		: Car(c), Driver(d), uber_city_(city) {
	}

	UberCar::UberCar(const UberCar& u)
		: Car(u), Driver(u), uber_city_(u.uber_city_) {
	}

	UberCar::~UberCar() {
	}

	void UberCar::PrintUberInfo() const {
		cout << "Uber in city: " << uber_city_ << "\n";
		Car::PrintCarInfo();
		Driver::PrintDriverInfo();
	}
	
	void UberCar::PrintCarInfo() const {
		PrintUberInfo();
	}

	void UberCar::PrintDriverInfo() const {
		PrintUberInfo();
	}
}