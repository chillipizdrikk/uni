#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;

class FootballPlayer {
private:
    string surname_;
    string club_;
    int goals_;

public:
    FootballPlayer();
    FootballPlayer(const std::string& surname, const std::string& club, int goals);
    FootballPlayer(const FootballPlayer& f);
    ~FootballPlayer();

    void print() const;
    string getClub() const;
    string getSurname() const;
    int getGoals() const;
    void setGoals(int goals);
    int calculateAnnualSalary() const;
    bool operator<(const FootballPlayer& other) const;
   
};
bool sortByGoals(const FootballPlayer& player1, const FootballPlayer& player2);
void readPlayersFromFile(const string& filename, vector<FootballPlayer>& players);
