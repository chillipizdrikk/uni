#include "candy.h"
using std::cout;

namespace goods {
	Candy::Candy()
		: candy_name_("")
		, candy_price_(0)
		, candy_weight_(0) {
	}

	Candy::Candy(const std::string& name, double price, double weight)
		: candy_name_(name)
		, candy_price_(price)
		, candy_weight_(weight) {
	}

	Candy::Candy(const Candy& c)
		: candy_name_(c.candy_name_)
		, candy_price_(c.candy_price_)
		, candy_weight_(c.candy_weight_) {
	}

	Candy::~Candy() {
	}

	char Candy::get_type() const {
		return 'C';
	}

	double Candy::get_price() const {
		return candy_weight_ * candy_price_;
	}

	std::string Candy::get_manufacturer() const {
		return candy_name_;
	}

	void Candy::Print() const {
		cout << candy_name_ << " candy\n";
		cout << "Weight: " << candy_weight_ << " kg.  ";
		cout << "Price (kg): " << candy_price_ << " uah\n";
		cout << "Total price: " << get_price() << " uah\n\n";
	}

	void Candy::ReadFrom(std::istream& in) {
		in >> candy_name_ >> candy_price_ >> candy_weight_;
	}

	void Candy::WriteTo(std::ostream& out) const {
		out << candy_name_ << ' ' << candy_price_ << ' ' << candy_weight_;
	}
}