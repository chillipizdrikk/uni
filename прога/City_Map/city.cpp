#include "city.h"
using namespace std;

City::City(const string& name, unsigned people)
	: city_name_(name)
	, city_people_(people) {
}

City::City(const City& c)
	: city_name_(c.city_name_)
	, city_people_(c.city_people_) {
}

City::~City() {
}

void City::Print() const {
	cout << city_name_ << " (" << city_people_ << " ppl)\n";
}

void City::ReadFrom(istream& in) {
	in >> city_name_ >> city_people_;
}

void City::WriteTo(ostream& out) const {
	out << city_name_ << ' ' << city_people_;
}

string City::get_name() const {
	return city_name_;
}

unsigned City::get_population() const {
	return city_people_;
}

istream& operator >> (istream& in, City& c) {
	c.ReadFrom(in);
	return in;
}

ostream& operator << (ostream& out, const City& c) {
	c.WriteTo(out);
	return out;
}