#ifndef SWEETS_CHOCOBAR_H_
#define SWEETS_CHOCOBAR_H_

#include "filling.h"
#include <string>

namespace sweets
{
	// Chocolate bar of fixed weigh with filling
	class ChocoBar : private Filling
	{
	public:
		ChocoBar();
		ChocoBar(const std::string& bar_name,
			const std::string& filling_type,
			int filling_weight,
			double bar_price);
		ChocoBar(const ChocoBar& c);
		virtual ~ChocoBar();

		void PrintFillingInfo() const override;
		void ReadFrom(std::istream& in) override;
		void WriteTo(std::ostream& out) const override;

		int CalculateWeight() const;
		double CalculatePrice() const;

	private:
		std::string name_; // Snickers, Nuts, Mars,...
		double price_; // price for the chocolate base
	};

	std::istream& operator>> (std::istream& in, ChocoBar& c);
	std::ostream& operator<< (std::ostream& out, const ChocoBar& c);
}

#endif // SWEETS_CHOCOBAR_H_