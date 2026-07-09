#include "list.h"
#include <fstream>

void printMovieList(const MovieList& lst)
{
    MovieNode* curr = lst.head;
    while (curr != nullptr)
    {
        cout << curr->data << "\n";
        curr = curr->next;
    }
    cout << "\n";
}

void addBack(MovieList& lst, const Movie& M)
{
    MovieNode* curr = lst.head;
    while (curr->next != nullptr)
    {
        curr = curr->next;
    }
    curr->next = new MovieNode(M);
}

void readMovieList(MovieList& lst, const string& fileName)
{
    ifstream iFile(fileName);

    if (lst.head == nullptr)
    {
        // list is empty        
        Movie M; iFile >> M;
        lst.head = new MovieNode(M);
    }



    MovieNode* curr = lst.head;
    while (curr->next != nullptr)
    {
        curr = curr->next;
    }



    // step 2 - read file, add to list
    while (!iFile.eof())
    {
        Movie M; iFile >> M;



        curr->next = new MovieNode(M);
        curr = curr->next;
    }



    iFile.close();
}

void addFront(MovieList& lst, const Movie& M)
{
    if (lst.head == nullptr)
    {
        lst.head = new MovieNode(M);
        return;
    }

    //list is not empty
    MovieNode* firstNode = new MovieNode(M);
    firstNode->next = lst.head;

    lst.head = firstNode;

    firstNode = nullptr;
}

void printMoviesFormatted(const MovieList& lst)
{
    if (lst.head == nullptr)
    {
        cout << "Movies list is empty.\n";
        return;
    }



    int maxTitleWidth = 0;
    int maxCountryWidth = 0;
    MovieNode* curr = lst.head;
    while (curr != nullptr)
    {
        int currTitleWidth = curr->data.movieTitle.length();
        int currCountryWidth = curr->data.movieCountry.length();
        if (currTitleWidth > maxTitleWidth) maxTitleWidth = currTitleWidth;
        if (currCountryWidth > maxCountryWidth) maxCountryWidth = currCountryWidth;



        curr = curr->next;
    }



    cout.width(maxTitleWidth); cout.setf(ios_base::right, ios_base::adjustfield);
    cout << "Title"; cout << " | ";
    cout.width(maxCountryWidth); cout.setf(ios_base::left, ios_base::adjustfield);
    cout << "Country"; cout << " | " << "BoxOffice\n";



    curr = lst.head;
    while (curr != nullptr)
    {
        printMovieFormatted(curr->data, maxTitleWidth, maxCountryWidth);
        curr = curr->next;
    }
    cout << "\n\n";
}


bool isFranceNotTaxi(const Movie& M)
{
    return M.movieCountry == "France" && M.movieTitle != "Taxi";
}



bool isUkraineTop(const Movie& M)
{
    return M.movieCountry == "Ukraine" && M.movieBoxOffice > 500000;
}


MovieNode* searchFirstBy(MovieList& lst, bool (*criteriaPtr)(const Movie&))
{
    if (lst.head == nullptr)
        return nullptr;



    MovieNode* curr = lst.head;
    while (curr != nullptr)
    {
        if (criteriaPtr(curr->data))
            return curr;



        curr = curr->next;
    }
    return nullptr;
}

