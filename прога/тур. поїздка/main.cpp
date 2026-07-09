#include <iostream>
#include "city.h"
#include "trip.h"
using namespace std;


int main()
{
    size_t n = 0;
    Trip* travelArr = readTripArray("travel.txt", n);
    sortTripArray(travelArr, n);
    printTripArray(travelArr, n);
    writeTripArray("result.txt", travelArr, n);

    size_t cityCount = 0;
    City* cityArr = new City[n];
    for (size_t i = 0; i < n; ++i)
    {
        if (!findCityInArray(cityArr, cityCount, travelArr[i].getTripDestination()))
        {
            cityArr[cityCount] = travelArr[i].getTripDestination();
            ++cityCount;
        }
    }
    cout << "\nDestinations\n";
    for (size_t i = 0; i < cityCount; ++i)
    {
        cout << i + 1 << ": " << cityArr[i].getCityName() << "\n";
    }
    cout << "\n\n";


    delete[] travelArr;
    return 0;

    /* City Lviv("Lviv", "Ukraine");
    City Kyiv("Kyiv", "Ukraine");
    City Paris("Paris", "France");
    City arr[3] = { Lviv, Paris, Kyiv };
    for (size_t i = 0; i < 3; ++i)
    {
        arr[i].printCityInfo();
    }
    cout << "\n\n";

    for (size_t i = 0; i < 3; ++i)
    {
        size_t M = i;
        for (size_t j = i + 1; j < 3; ++j)
        {
            if (arr[j] < arr[M])
                M = j;
        }

        if (M != i)
        {
            City temp = arr[i];
            arr[i] = arr[M];
            arr[M] = temp;
        }
    }
    for (size_t i = 0; i < 3; ++i)
    {
        arr[i].printCityInfo();
    }
    cout << "\n\n";*/

}
