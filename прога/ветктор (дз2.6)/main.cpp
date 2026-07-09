#include <iostream>
#include "player.h"
using namespace std;

int main() {
    cout << "------Task 1------\n\n";
    FootballPlayer player1("Ronaldo", "Juventus", 30);
    FootballPlayer player2("Messi", "Barcelona", 25);

    player1.print();
    cout << "Annual Ronaldo salary: " << player1.calculateAnnualSalary() << " $\n\n";

    player2.print();
    std::cout << "Annual Messi salary: " << player2.calculateAnnualSalary() << " $\n\n";

    if (player1 < player2) {
        cout << "Ronaldo earns less than Messi" << "\n";
    }
    else {
        std::cout << "Ronaldo earns more than Messi" << "\n";
    }
    cout << "\n------Task 2------\n\n";
    std::vector<FootballPlayer> allPlayers;
    std::vector<FootballPlayer> barcelonaPlayers;
    std::vector<FootballPlayer> manchesterPlayers;
    std::vector<FootballPlayer> juventusPlayers;

    readPlayersFromFile("players1.txt", allPlayers);
    readPlayersFromFile("players2.txt", allPlayers);
    readPlayersFromFile("players3.txt", allPlayers);

    sort(allPlayers.begin(), allPlayers.end());

    for (const auto& player : allPlayers) {
        if (player.getClub() == "Barcelona") {
            barcelonaPlayers.push_back(player);
        }
        else if (player.getClub() == "Manchester") {
            manchesterPlayers.push_back(player);
        }
        else if (player.getClub() == "Juventus") {
            juventusPlayers.push_back(player);
        }
    }
    cout << "All players:\n";
    for (const auto& player : allPlayers) {
        player.print();
        cout << "\n";
    }

    if (!barcelonaPlayers.empty()) {
        auto maxBarcelonaPlayer = max_element(barcelonaPlayers.begin(), barcelonaPlayers.end());
        cout << "Max Barcelona Player:\n";
        maxBarcelonaPlayer->print();
        cout << "\n";
    }

    if (!manchesterPlayers.empty()) {
        auto maxManchesterPlayer = max_element(manchesterPlayers.begin(), manchesterPlayers.end());
        cout << "Max Manchester Player:\n";
        maxManchesterPlayer->print();
        cout << "\n";
    }

    if (!juventusPlayers.empty()) {
        auto maxJuventusPlayer = std::max_element(juventusPlayers.begin(), juventusPlayers.end());
        cout << "Max Juventus Player:\n";
        maxJuventusPlayer->print();
        cout << "\n";
    }
    cout << "------Task 3------\n\n";
    for (auto& player : allPlayers) {
        player.setGoals(player.getGoals() * 2);
    }
    ofstream outputFile("updated_players.txt");
    if (outputFile.is_open()) {
        for (const auto& player : allPlayers) {
            outputFile << player.getSurname() << "," << player.getClub() << "," << player.getGoals() << "\n";
        }
        outputFile.close();
        cout << "\n";
    }
    else {
        cout << "Error\n";
    }
    sort(allPlayers.begin(), allPlayers.end(), sortByGoals);
    cout << "Three players with the fewest goals:\n";
    for (int i = 0; i < 3 && i < allPlayers.size(); i++) {
        allPlayers[i].print();
        cout << "\n";
    }

    std::vector<FootballPlayer> uniqueClubPlayers;
    std::vector<std::string> uniqueClubs;

    for (const auto& player : allPlayers) {
        if (std::find(uniqueClubs.begin(), uniqueClubs.end(), player.getClub()) == uniqueClubs.end()) {
            uniqueClubs.push_back(player.getClub());
            uniqueClubPlayers.push_back(player);
        }
    }

    cout << "Players from each club:\n";
    for (const auto& player : uniqueClubPlayers) {
        player.print();
        cout << "\n";
    }


    return 0;
}