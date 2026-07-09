#include<iostream>
#include "movie.h"
#include "list.h"
using namespace std;


int main()
{
    /*
    Movie M1;
    Movie M2("HarryPotter", "USA/GB", 780900);
    Movie M3(M2); M3.movieTitle = "LordOfTheRings";
    cout << "Enter movie info\n"; cin >> M1;

    cout << "My movies: " << M1 << "\n" << M2 << "\n" << M3 << "\n\n";
    */
    /*
    size_t n;
    Movie* cinema = readFromFile("imdb.txt", n);
    sortByCountries(cinema, n);
    printMovies(cinema, n);

    //UKR USA FR
    Movie* ukrBegin = cinema;
    Movie* usaBegin = findMovieByCountry(cinema, n, "USA");
    Movie* frBegin = findMovieByCountry(cinema, n, "France");

    Movie* ukrEnd = usaBegin - 1;
    Movie* usaEnd = frBegin - 1;
    Movie* frEnd = cinema + n - 1;

    cout << "UKRAINE\n";
    printMoviesRange(ukrBegin, ukrEnd);
    Movie* maxM = findMaxMovieInRange(ukrBegin, ukrEnd);
    cout << "MAX is: " << *maxM << "\n\n";


    cout << "USA\n";
    printMoviesRange(usaBegin, usaEnd);
    maxM = findMaxMovieInRange(usaBegin, usaEnd);
    cout << "MAX is: " << *maxM << "\n\n";


    cout << "FRANCE\n";
    printMoviesRange(frBegin, frEnd);
    maxM = findMaxMovieInRange(frBegin, frEnd);
    cout << "MAX is: " << *maxM << "\n\n";


    //sortMovies(cinema, n, compareByPrices);
    //printMovies(cinema, n);



    delete[] cinema;
    */
    
    Movie M1("Taxi", "France", 290100);
    Movie M2("LordOfTheRings", "USA", 1200150);
    Movie M3("Voron", "Ukraine", 400050);



    cout.width(20); cout.setf(ios_base::right, ios_base::adjustfield); cout << "Title"; cout << " | ";
    cout.width(10); cout.setf(ios_base::left, ios_base::adjustfield); cout << "Country"; cout << " | " << "BoxOffice\n";

    printMovieFormatted(M1, 20, 10);
    printMovieFormatted(M2, 20, 10);
    printMovieFormatted(M3, 20, 10);

    cout << "\n\n";


    //MovieNode N3(M3);
    //N1.next = &N2;
    //N2.next = &N3;
    //MovieList myList(&N1);
    //printMovieList(myList);

    MovieList myList;
    addFront(myList, M1);
    addFront(myList, M2);
    addFront(myList, M3);
    readMovieList(myList, "listinfo.txt");
    printMoviesFormatted(myList);
    cout << "\n\n";

    MovieNode* franceNode = searchFirstBy(myList, isFranceNotTaxi);
    MovieNode* ukraineNode = searchFirstBy(myList, isUkraineTop);
    if (franceNode != nullptr)
    {
        cout << "France criteria OK: " << franceNode->data << "\n";
    }
    if (ukraineNode != nullptr)
    {
        cout << "Ukraine criteria OK: " << ukraineNode->data << "\n";
    }




    return 0;
}