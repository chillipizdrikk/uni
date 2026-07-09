#include "choco_bar.h"

using std::cout;

namespace sweets
{
	ChocoBar::ChocoBar()
		: Filling()
		, name_(""), price_(0.0)
	{}

	ChocoBar::ChocoBar(const std::string& bar_name, const std::string& filling_type,
		int filling_weight, double bar_price)
		: Filling(filling_type, filling_weight)
		, name_(bar_name), price_(bar_price)
	{}

	ChocoBar::ChocoBar(const ChocoBar& c)
		: Filling(c)
		, name_(c.name_), price_(c.price_)
	{}

	ChocoBar::~ChocoBar()
	{}

	void ChocoBar::PrintFillingInfo() const
	{
		// Chocolate bar: Mars
		// Filling: Caramel (50 gr)
		// Weight: 150 gr Price: 32.5 uah
		cout << "Chocolate bar: " << name_ << "\n";
		cout << "Filling: "; Filling::PrintFillingInfo();
		cout << "Weight: " << CalculateWeight() << " gr. ";
		cout << "Price: " << CalculatePrice() << " uah\n";
	}

	void ChocoBar::ReadFrom(std::istream& in)
	{
		// Mars Caramel 50 32.5
		in >> name_; Filling::ReadFrom(in); in >> price_;
	}

	void ChocoBar::WriteTo(std::ostream& out) const
	{
		// Mars Caramel 50 32.5
		out << name_ << ' '; Filling::WriteTo(out); out << ' ' << price_;
	}

	int ChocoBar::CalculateWeight() const
	{
		return get_weight() + 85;
	}

	double ChocoBar::CalculatePrice() const
	{
		double filling_price = price_ / 100.0 * (double)get_weight();
		return price_ + filling_price;
	}

	std::istream& operator>> (std::istream& in, ChocoBar& c)
	{
		c.ReadFrom(in);
		return in;
	}

	std::ostream& operator<< (std::ostream& out, const ChocoBar& c)
	{
		c.WriteTo(out);
		return out;
	}
}