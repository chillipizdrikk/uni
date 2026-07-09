#pragma once
#include <string>
#include <iostream>
using namespace std;

struct Movie
{
    string movieTitle;
    string movieCountry;
    int movieBoxOffice;

    Movie() : movieTitle(""), movieCountry(""), movieBoxOffice(0) {}
    Movie(const string& title, const string& country, int boxOffice)
        : movieTitle(title), movieCountry(country), movieBoxOffice(boxOffice) {}
    Movie(const Movie& M)
        : movieTitle(M.movieTitle), movieCountry(M.movieCountry), movieBoxOffice(M.movieBoxOffice) {}
};

istream& operator>>(istream& in, Movie& M);
ostream& operator<<(ostream& out,const Movie& M);

void printMovieFormatted(const Movie& M, int titleWidth, int countryWidth);

Movie* readFromFile(const string& fileName, size_t& n);
void printMovies(const Movie* arr, size_t n);

bool compareByCountries(const Movie& M1, const Movie& M2);
bool compareByPrices(const Movie& M1, const Movie& M2);

void sortMovies(Movie* arr, size_t n, bool(*ptrCompare)(const Movie&, const Movie&));
void sortByCountries(Movie* arr, size_t n);

//return pointer to first Movie with the given country
Movie* findMovieByCountry(Movie* arr, size_t n, const string& country);

//??? [arrBegin, arrEnd]
void printMoviesRange(Movie* arrBegin, Movie* arrEnd);
Movie* findMaxMovieInRange(Movie* arrBegin, Movie* arrEnd);


