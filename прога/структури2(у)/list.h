#pragma once
#include"movie.h"

struct MovieNode
{
	Movie data;
	MovieNode* next;

	MovieNode(): data(), next(nullptr) {}
	MovieNode(const Movie& M) : data(M),next(nullptr) {}
	MovieNode(const MovieNode& N) : data(N.data), next(nullptr) {}
};

struct MovieList
{
	MovieNode* head;



	MovieList() :head(nullptr) {}
	MovieList(MovieNode* headNode) : head(headNode) {}
};

void printMovieList(const MovieList& lst);
void addBack(MovieList& lst, const Movie& M);
void addFront(MovieList& lst, const Movie& M);

void readMovieList(MovieList& lst, const string& fileName);

void printMoviesFormatted(const MovieList& lst);


bool isFranceNotTaxi(const Movie& M); // France, but not Taxi
bool isUkraineTop(const Movie& M); // Ukraine, but > 500'000
MovieNode* searchFirstBy(MovieList& lst, bool(*criteriaPtr)(const Movie&));