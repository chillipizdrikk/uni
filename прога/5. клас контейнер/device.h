#pragma once
#include "product.h"

namespace goods {
	class Device : public Product {
	public:
		Device();
		Device(const std::string& brand, const std::string& name, double price);
		Device(const Device& d);
		virtual ~Device();

		char get_type() const override;
		double get_price() const override;
		std::string get_manufacturer() const override;
		void Print() const override;
		void ReadFrom(std::istream& in) override;
		void WriteTo(std::ostream& out) const override;

	private:
		std::string device_brand_;
		std::string device_name_;
		double device_price_;
	};
}
