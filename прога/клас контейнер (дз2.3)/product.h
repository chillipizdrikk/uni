#pragma once
#include <iostream>
#include <string>

namespace goods {
	class Product {
	public:
		virtual ~Product();

		virtual char get_type() const abstract;
		virtual double get_price() const abstract;
		virtual std::string get_manufacturer() const abstract;
		virtual void Print() const abstract;
		virtual void ReadFrom(std::istream& in) abstract;
		virtual void WriteTo(std::ostream& out) const abstract;
		
		bool operator< (const Product& p) const;

		/*virtual Product* Clone() const abstract;*/
	};

	std::istream& operator >> (std::istream& in, Product& p);
	std::ostream& operator << (std::ostream& out, const Product& p);
}
