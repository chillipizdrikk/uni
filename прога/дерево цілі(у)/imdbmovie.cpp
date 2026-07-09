#include "imdbmovie.h"
using namespace std;

ImdbMovie::ImdbMovie() : name(""), rate(0.0)
{}

ImdbMovie::ImdbMovie(const string& nm, double rt) : name(nm), rate(rt)
{}

ImdbMovie::ImdbMovie(const ImdbMovie& M) : name(M.name), rate(M.rate)
{}

ImdbMovie::~ImdbMovie()
{}

void ImdbMovie::read()
{
	cout << "Enter movie name: "; cin >> name;
	cout << "Enter movie rate: "; cin >> rate;
}


void ImdbMovie::print()
{
	cout << "Movie: " << name << " Imdb: " << rate << "\n";
}


string ImdbMovie::getName() const
{
	return name;
}


double ImdbMovie :: getRate() const
{
	return rate;
}


void ImdbMovie::setName(const std::string& movieName)
{
	name = movieName;
}



void ImdbMovie::setRate(double movieRate)
{
	rate = movieRate;
}



void ImdbMovie::modifyRate(double rateChange)
{
	rate += rateChange;
}


std::string& ImdbMovie::getName()
{
	return name;
}



double& ImdbMovie::getRate()
{
	return rate;
}



std::istream& operator>>(std::istream& in, ImdbMovie& M)
{
	in >> M.getName() >> M.getRate();
	return in;
}



std::ostream& operator<<(std::ostream& out, const ImdbMovie& M)
{
	out << M.getName() << ' ' << M.getRate();
	return out;
}