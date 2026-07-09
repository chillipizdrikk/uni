#include "car.h"
using namespace std;

namespace algo {
	Car::Car()
		: car_brand_("no brand"), car_price_(0) {
	}

	Car::Car(const string& brand, double price)
		: car_brand_(brand), car_price_(price) {
	}

	Car::Car(const Car& c)
		: car_brand_(c.car_brand_), car_price_(c.car_price_) {
	}

	Car::~Car() {
	}

	double Car::get_price() const {
		return car_price_;
	}

	void Car::Print() const {
		cout << "Brand: " << car_brand_;
		cout << " Price: " << car_price_ << " uah\n";
	}

	void Car::set_price(double price) {
		car_price_ = price;
	}

	void Car::ReadFrom(std::istream& in) {
		in >> car_brand_ >> car_price_;
	}

	void Car::WriteTo(std::ostream& out) const
	{
		out << "Car: " << car_brand_ << ' ' << car_price_ << " uah\n";
	}

	std::istream& operator>>(std::istream& in, Car& c)
	{
		c.ReadFrom(in);
		return in;
	}

	std::ostream& operator<<(std::ostream& out, const Car& c)
	{
		c.WriteTo(out);
		return out;
	}

	std::string Car::get_brand() const {
		return car_brand_;
	}

	void Car::set_brand(const std::string& brand) {
		car_brand_ = brand;
	}

	bool Car::operator>(const Car& c) const
	{
		return get_price() > c.get_price();
	}

	bool Car::operator==(const Car& c) const
	{
		return get_brand() == c.get_brand();
	}
}