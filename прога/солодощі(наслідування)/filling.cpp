#include "filling.h"

using std::cout;

namespace sweets
{
	Filling::Filling()
		: type_(""), weight_(0)
	{}

	Filling::Filling(const std::string& filling_type, int filling_weight)
		: type_(filling_type), weight_(filling_weight)
	{}

	Filling::Filling(const Filling& f)
		: type_(f.type_), weight_(f.weight_)
	{}

	Filling::~Filling()
	{}

	void Filling::PrintFillingInfo() const
	{
		cout << type_ << " (" << weight_ << " gr)\n";
	}

	void Filling::ReadFrom(std::istream& in)
	{
		in >> type_ >> weight_;
	}

	void Filling::WriteTo(std::ostream& out) const
	{
		out << type_ << ' ' << weight_;
	}

	const std::string& Filling::get_type() const
	{
		return type_;
	}

	int Filling::get_weight() const
	{
		return weight_;
	}

	void Filling::set_type(const std::string& filling_type)
	{
		type_ = filling_type;
	}

	void Filling::set_weight(int filling_weight)
	{
		if (filling_weight < 0)
			return;

		weight_ = filling_weight;
	}

	std::istream& operator>> (std::istream& in, Filling& f)
	{
		f.ReadFrom(in);
		return in;
	}

	std::ostream& operator<< (std::ostream& out, const Filling& f)
	{
		f.WriteTo(out);
		return out;
	}
}