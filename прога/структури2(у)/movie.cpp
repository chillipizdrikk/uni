#include"movie.h"
#include <fstream>
istream& operator>>(istream& in, Movie& M)
{
    in >> M.movieTitle >> M.movieCountry >> M.movieBoxOffice;
    return in;
}



ostream& operator<<(ostream& out, const Movie& M)
{
    out << M.movieTitle << ' ' << M.movieCountry << ' ' << M.movieBoxOffice;
    return out;
}

Movie* readFromFile(const string& fileName, size_t& n)
{
    ifstream iFile(fileName);
    iFile >> n;
    Movie* arr = new Movie[n];
    for (size_t i = 0; i < n; ++i)
    {
        iFile >> arr[i];
    }
    iFile.close();
    return arr;
}

void printMovies(const Movie* arr, size_t n)
{
    cout << "Movies collection\n";
    for (size_t i = 0; i < n; ++i)
    {
        cout << arr[i] << "\n";
    }
    cout << "\n\n";
}


bool compareByCountries(const Movie& M1, const Movie& M2) //M1<M2
{
    return M1.movieCountry < M2.movieCountry;
}


bool compareByPrices(const Movie& M1, const Movie& M2)
{
    return M1.movieBoxOffice < M2.movieBoxOffice;
}

void sortMovies(Movie* arr, size_t n, bool (*ptrCompare)(const Movie&, const Movie&))
{
    for (size_t i = 0; i < n; ++i)
    {
        size_t minIndex = i;
        for (size_t j = i + 1; j < n; ++j)
        {
            if (ptrCompare(arr[minIndex], arr[j]))
            {
                minIndex = j;
            }
        }



        if (minIndex != i)
        {
            Movie temp = arr[i];
            arr[i] = arr[minIndex];
            arr[minIndex] = temp;
        }
    }
}

void sortByCountries(Movie* arr, size_t n)
{
    for (size_t i = 0; i < n; ++i)
    {
        size_t maxIndex = i;
        for (size_t j = i + 1; j < n; ++j)
        {
            if (arr[j].movieCountry > arr[maxIndex].movieCountry)
            {
                maxIndex = j;
            }
        }



        if (maxIndex != i)
        {
            Movie temp = arr[i];
            arr[i] = arr[maxIndex];
            arr[maxIndex] = temp;
        }
    }
}



Movie* findMovieByCountry(Movie* arr, size_t n, const string& country)
{
    for (size_t i = 0; i < n; ++i)
    {
        if (arr[i].movieCountry == country)
        {
            return &arr[i];
        }
    }
    return nullptr;
}

void printMoviesRange(Movie* arrBegin, Movie* arrEnd)
{
    while (arrBegin != arrEnd)
    {
        cout << *arrBegin << "\n";
        ++arrBegin;
    }
    cout << *arrEnd << "\n\n";
}

Movie* findMaxMovieInRange(Movie* arrBegin, Movie* arrEnd)
{
    Movie* max = arrBegin;
    ++arrBegin;
    while (arrBegin != arrEnd)
    {
        if (arrBegin->movieBoxOffice > max->movieBoxOffice)
        {
            max = arrBegin;
        }
        ++arrBegin;
    }
    if (arrEnd->movieBoxOffice > max->movieBoxOffice)
    {
        max = arrEnd;
    }
    return max;
}

void printMovieFormatted(const Movie& M, int titleWidth, int countryWidth)
{
    cout.width(titleWidth); cout.setf(ios_base::right, ios_base::adjustfield);
    cout << M.movieTitle; cout << " | ";



    cout.width(countryWidth); cout.setf(ios_base::left, ios_base::adjustfield);
    cout << M.movieCountry; cout << " | " << M.movieBoxOffice << "\n";
}