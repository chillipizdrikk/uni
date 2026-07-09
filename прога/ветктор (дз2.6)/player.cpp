#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>

#include"player.h"
using namespace std;

FootballPlayer::FootballPlayer()
    : surname_(""), club_(""), goals_(0) {}

FootballPlayer::FootballPlayer(const std::string& surname, const std::string& club, int goals)
    : surname_(surname), club_(club), goals_(goals) {}

FootballPlayer::FootballPlayer(const FootballPlayer& f)
    : surname_(f.surname_), club_(f.club_), goals_(f.goals_) {}

FootballPlayer::~FootballPlayer()
{}

void FootballPlayer::print() const {
    cout << "Surname: " << surname_ << "\n";
    cout << "Club: " << club_ << "\n";
    cout << "Goals scored: " << goals_ << "\n";
}

int FootballPlayer::calculateAnnualSalary() const {
    return goals_ * 100;
}

bool FootballPlayer::operator<(const FootballPlayer& other) const {
    return calculateAnnualSalary() < other.calculateAnnualSalary();
}

void readPlayersFromFile(const string& filename, vector<FootballPlayer>& players) {
    ifstream file(filename);
    if (file.is_open()) {
        string surname, club;
        int goals;
        while (file >> surname >> club >> goals) {
            players.emplace_back(surname, club, goals);
        }
        file.close();
    }
    else {
        cout << "Cannot open file: " << filename << "\n";
    }
}

string FootballPlayer::getClub() const {
    return club_;
}

string FootballPlayer::getSurname() const {
    return surname_;
}

int FootballPlayer::getGoals() const {
    return goals_;
}

void FootballPlayer::setGoals(int goals) {
    goals_ = goals;
}

bool sortByGoals(const FootballPlayer& player1, const FootballPlayer& player2) {
    return player1.getGoals() < player2.getGoals();
}