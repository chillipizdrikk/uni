#ifndef SWEETS_FILLING_H_
#define SWEETS_FILLING_H_

#include <iostream>
#include <string>

namespace sweets
{
	// Filling of a chocolate bar
	class Filling
	{
	public:
		Filling();
		Filling(const std::string& filling_type, int filling_weight);
		Filling(const Filling& f);
		virtual ~Filling();

		virtual void PrintFillingInfo() const;
		virtual void ReadFrom(std::istream& in);
		virtual void WriteTo(std::ostream& out) const;

		int get_weight() const;

	protected:
		const std::string& get_type() const;

		void set_type(const std::string& filling_type);
		void set_weight(int filling_weight);

	private:
		std::string type_; // caramel, nuts, etc
		int weight_; // in grams

	};

	std::istream& operator>> (std::istream& in, Filling& f);
	std::ostream& operator<< (std::ostream& out, const Filling& f);
}

#endif // SWEETS_FILLING_H_