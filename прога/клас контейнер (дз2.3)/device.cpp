#include "device.h"
using std::cout;

namespace goods {
	Device::Device()
		: device_brand_("")
		, device_name_("")
		, device_price_(0) {
	}

	Device::Device(const std::string& brand, const std::string& name, double price)
		: device_brand_(brand)
		, device_name_(name)
		, device_price_(price) {
	}

	Device::Device(const Device& d)
		: device_brand_(d.device_brand_)
		, device_name_(d.device_name_)
		, device_price_(d.device_price_) {
	}

	Device::~Device() {
	}

	char Device::get_type() const {
		return 'D';
	}

	double Device::get_price() const {
		return device_price_;
	}

	std::string Device::get_manufacturer() const {
		return device_brand_;
	}

	void Device::Print() const {
		cout << device_name_ << " Brand: " << device_brand_ << "\n";
		cout << "Price: " << device_price_ << " uah\n\n";
	}

	void Device::ReadFrom(std::istream& in) {
		in >> device_brand_ >> device_name_ >> device_price_;
	}

	void Device::WriteTo(std::ostream& out) const {
		out << device_brand_ << ' ' << device_name_ << ' ' << device_price_;
	}

	/*Product* Device::Clone() const {
		return new Device(*this);
	}*/
}