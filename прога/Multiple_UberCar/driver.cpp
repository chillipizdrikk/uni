#include "driver.h"
#include <iostream>
using std::cout;
using std::string;

namespace taxi {
	Driver::Driver()
		: driver_name_("vacancy"), driver_age_(18) {
	}

	Driver::Driver(const std::string& name, unsigned age)
		:driver_name_(name), driver_age_(age >= 18 ? age : 18) {
	}

	Driver::Driver(const Driver& d)
	: driver_name_(d.driver_name_), driver_age_(d.driver_age_) {
	}
	Driver:: ~Driver() {
	}

	string Driver::get_driver_name() const {
		return driver_name_;
	}
	void Driver::PrintDriverInfo() const {
		cout << "Driver: " << driver_name_;
		cout << " (Age: " << driver_age_ << " years)\n";
	}
}
