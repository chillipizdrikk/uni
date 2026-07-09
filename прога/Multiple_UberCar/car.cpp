#include "car.h"
#include <iostream>
using std::string;
using std::cout;


namespace taxi {
	Car::Car()
		: car_brand_("Audi"), car_price_(1000) {
	}

	Car::Car(const std::string& brand, double price)
		: car_brand_(brand), car_price_(price) {
	}

	Car::Car(const Car& c)
		: car_brand_(c.car_brand_), car_price_(c.car_price_) {
	}

	Car::~Car() {
	}

	string Car::get_car_brand() const {
		return car_brand_;
	}

	void Car::PrintCarInfo() const {
		cout << "Auto: " << car_brand_ << " Price: " << car_price_ << " uah\n";
	}
}