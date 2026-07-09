#include <algorithm>
#include <iostream>
#include <fstream>
#include <map>
#include <set>
#include "city.h"
using namespace std;

int main() {
    map<string, City> countries;
    ifstream fin("world.txt");
    while (!fin.eof()) {
        string country; fin >> country;
        City city; fin >> city;
        countries.emplace(make_pair(country, city));
    }
    fin.close();

    cout << "World capitals\n";
    for_each(countries.cbegin(), countries.cend(),
        [](const pair<string, City>& country_pair) {
            cout << country_pair.first << " Capital: ";
            country_pair.second.Print();
        });
    cout << "\n";

    // find biggest capital --> create set of capitals from countries
    set<City> caps;
    for (auto it = countries.cbegin(); it != countries.cend(); ++it) {
        caps.insert(it->second);
    }
    cout << "Biggest capital is: "; caps.crbegin()->Print();
    cout << "\n";

    // find country of this capital
    for (auto it = countries.cbegin(); it != countries.cend(); ++it) {
        if (it->second.get_name() == caps.crbegin()->get_name()) {
            cout << "Country is: " << it->first << "\n\n";
            break;
        }
    }

    // find coutry with smallest capital
    // --> map <population - coutry>
    map<unsigned, string> population;
    for (auto it = countries.cbegin(); it != countries.cend(); ++it) {
        population.emplace(make_pair(it->second.get_population(), it->first));
    }
    cout << "Smallest capital: " << population.cbegin()->second;
    cout << " (" << population.cbegin()->first << " ppl)\n";
    cout << "Biggest capital:  " << population.crbegin()->second;
    cout << " (" << population.crbegin()->first << " ppl)\n";



    /*City lviv("Lviv", 800500);
    City kyiv("Kyiv", 4000000);

    map<string, double> imdb;
    imdb["Film1"] = 6.5; // added new element
    imdb["Film2"] = 8.1;
    imdb["Film1"] = 9.2; // modified existing element
    imdb["Film2"] += 0.4;
    cout << "My Film 1: " << imdb["Film1"] << "\n";
    cout << "My Film 2: " << imdb["Film2"] << "\n";
    cout << "My Film 3: " << imdb["Film3"] << "\n\n";
    imdb.insert(pair<string, double>("Film4", 3.2));
    imdb.insert({ "Film5", 4.7 });
    imdb.insert(make_pair("Film6", 7.1));
    cout << "Imdb movies rate (" << imdb.size() << " movies)\n";
    for (auto it = imdb.cbegin(); it != imdb.cend(); ++it) {
        //map<string, double>::const_iterator
        cout << "Movie: " << it->first;
        cout << "Rate: " << it->second << "\n";
    }
    cout << "\n\n";

    map<string, unsigned> city_map;
    ifstream fin("capitals.txt");
    while (!fin.eof()) {
        string city_name;
        unsigned city_population;
        fin >> city_name >> city_population;
        city_map.emplace(make_pair(city_name, city_population));
    }
    fin.close();
    cout << "Map of capitals: \n";
    for_each(city_map.cbegin(), city_map.cend(),
        [](const auto& city_pair) {
            cout << "Capital: " << city_pair.first;
            cout << " Population: " << city_pair.second << "\n";
        });
    cout << "\n\n";

    //result is <iterator, bool>
    //iterator points at pair <string, unsigned>
    auto result = city_map.insert({ "Kyiv", 4000000 });
    if (result.second) {
        cout << "Element ADDED!\n";
        cout << "City: " << result.first->first;
        cout << "Population: " << result.first->second << "\n";

    }*/

    /*set<int> num = {2, 8, 10, 2, 5, 8, 10, 4}; // 8 elem
    cout << "num size: " << num.size() << "\n";
    for (set<int>::const_iterator it = num.cbegin(); it != num.cend(); ++it) {
        cout << *it << ' ';
    }
    cout << "\n\n";

    set<City> capitals;
    capitals.insert(lviv);
    capitals.insert(kyiv);

    ifstream fin("capitals.txt");
    while (!fin.eof()) {
        City c; fin >> c;
        capitals.insert(c);
    }
    fin.close();

    cout << "Set of capitals (" << capitals.size() << " cities)\n";
    for (set<City>::const_iterator it = capitals.cbegin(); it != capitals.cend(); ++it) {
        it->Print();
    }
    cout << "\n\n";

    cout << "Test COUNT\n";
    cout << "count (10) in numbers: " << num.count(10) << "\n";
    cout << "count (15) in numbers: " << num.count(15) << "\n\n";

    cout << "count (Lviv) in Cities: " << capitals.count(lviv) << "\n";
    cout << "count (Ternopil) in Cities: " << capitals.count(City("Ternopil", 290200)) << "\n\n";

    auto kyiv_it = capitals.find(kyiv);
    if (kyiv_it != capitals.end()) {
        cout << "Kyiv found! Population: ";
        cout << kyiv_it->get_population() << "\n\n";
    } */


    return 0;
}