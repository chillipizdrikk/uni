#pragma once
#pragma once
#include <string>
#include <iostream>

namespace algo {
	class Car {
	public:
		Car();
		Car(const std::string& brand, double price);
		Car(const Car& c);
		~Car();

		void Print() const;
		double get_price() const;
		void set_price(double price);
		std::string get_brand() const;
		void set_brand(const std::string& brand);

		void ReadFrom(std::istream& in);
		void WriteTo(std::ostream& out) const;

		bool operator>(const Car& c) const;
		bool operator==(const Car& c) const;

	private:
		std::string car_brand_;
		double car_price_;
	};

	std::istream& operator>>(std::istream& in, Car& c);
	std::ostream& operator<<(std::ostream& out, const Car& c);
}