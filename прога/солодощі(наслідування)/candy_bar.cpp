#include "candy_bar.h"

using std::cout;

namespace sweets
{
	CandyBar::CandyBar()
		: name_(""), price_(0), filling_()
	{}

	CandyBar::CandyBar(const std::string& candy_name,
		const std::string& filling_type,
		int filling_weight,
		double candy_price)
		: name_(candy_name), price_(candy_price), filling_(filling_type, filling_weight)
	{}

	CandyBar::CandyBar(const std::string& candy_name,
		const Filling& candy_filling,
		double candy_price)
		: name_(candy_name), price_(candy_price), filling_(candy_filling)
	{}

	CandyBar::CandyBar(const CandyBar& c)
		: name_(c.name_), price_(c.price_), filling_(c.filling_)
	{}

	CandyBar::~CandyBar()
	{}

	void CandyBar::PrintCandyInfo() const
	{
		// Candy bar: Mars
		// Filling: Caramel (50 gr)
		// Weight: 150 gr Price: 32.5 uah
		cout << "Candy bar: " << name_ << "\n";
		filling_.PrintFillingInfo();
		cout << "Weight: " << CalculateCandyWeight() << " gr. ";
		cout << "Price: " << CalculateCandyPrice() << " uah\n";
	}

	void CandyBar::ReadCandyFrom(std::istream& in)
	{
		// Mars Caramel 50 32.5
		in >> name_ >> filling_ >> price_;
	}

	void CandyBar::WriteCandyTo(std::ostream& out) const
	{
		// Mars Caramel 50 32.5
		out << name_ << ' ' << filling_ << ' ' << price_;
	}

	int CandyBar::CalculateCandyWeight() const
	{
		return 85 + filling_.get_weight();
	}

	double CandyBar::CalculateCandyPrice() const
	{
		double filling_price = price_ / 100.0 * (double)filling_.get_weight();
		return price_ + filling_price;
	}

	std::istream& operator>> (std::istream& in, CandyBar& c)
	{
		c.ReadCandyFrom(in);
		return in;
	}

	std::ostream& operator<< (std::ostream& out, const CandyBar& c)
	{
		c.WriteCandyTo(out);
		return out;
	}
}