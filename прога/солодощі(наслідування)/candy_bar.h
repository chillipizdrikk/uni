#ifndef SWEETS_CANDYBAR_H_
#define SWEETS_CANDYBAR_H_

#include <iostream>
#include <string>
#include "filling.h"

namespace sweets
{
	// Another chocolate bar with filling - implemented via Has-A
	class CandyBar
	{
	public:
		CandyBar();
		CandyBar(const std::string& candy_name,
			const std::string& filling_type,
			int filling_weight,
			double candy_price);
		CandyBar(const std::string& candy_name,
			const Filling& candy_filling,
			double candy_price);
		CandyBar(const CandyBar& c);
		~CandyBar();

		void PrintCandyInfo() const;
		void ReadCandyFrom(std::istream& in);
		void WriteCandyTo(std::ostream& out) const;

		int CalculateCandyWeight() const;
		double CalculateCandyPrice() const;

	private:
		std::string name_;
		double price_;
		Filling filling_;
	};

	std::istream& operator>> (std::istream& in, CandyBar& c);
	std::ostream& operator<< (std::ostream& out, const CandyBar& c);
}

#endif // SWEETS_CANDYBAR_H_
