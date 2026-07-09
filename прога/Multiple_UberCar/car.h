#pragma once
#include <string>

namespace taxi {
	class Car {
	public:
		Car();
		Car(const std::string& brand, double price);
		Car(const Car& c);
		virtual ~Car();

		std::string get_car_brand() const;
		virtual void PrintCarInfo() const;

	private:
		std::string car_brand_;
		double car_price_;
	};
}