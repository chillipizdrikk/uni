#include "product.h"
#include <fstream>

namespace goods {
	Product::~Product() {
	}

	bool Product::operator< (const Product& p) const {
		return get_price() < p.get_price();
	}

	std::istream& operator >> (std::istream& in, Product& p) {
		p.ReadFrom(in);
		return in;
	}

	std::ostream& operator << (std::ostream& out, const Product& p) {
		p.WriteTo(out);
		return out;
	}
}