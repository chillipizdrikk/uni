#pragma once
#include "product.h"

namespace goods {
	class Candy : public Product {

	public:
		Candy();
		Candy(const std::string& name, double price, double weight);
		Candy(const Candy& c);
		virtual ~Candy();

		char get_type() const override;
		double get_price() const override;
		std::string get_manufacturer() const override;
		void Print() const override;
		void ReadFrom(std::istream& in) override;
		void WriteTo(std::ostream& out) const override;

	private:
		std::string candy_name_;
		double candy_price_; // for 1 kg
		double candy_weight_;
	};
}