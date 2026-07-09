#pragma once
#include "car.h"
#include "driver.h"


namespace taxi {
	class UberCar :public Car, public Driver {
	public:
		UberCar();
		UberCar(const std::string& city,
			const std::string& brand,
			double price,
			const std::string& name,
			unsigned age);
		UberCar(const std::string& city, const Car& c, const Driver& d);
		UberCar(const UberCar& u);
		virtual ~UberCar();

		void PrintUberInfo() const;
		void PrintCarInfo() const override;
		void PrintDriverInfo() const override;

	private:
		std::string uber_city_;
	};
}