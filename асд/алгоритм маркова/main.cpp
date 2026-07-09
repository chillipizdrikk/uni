#include <iostream>
#include <string>
#include <vector>

using namespace std;

string markov(const vector<string>& u, const vector<string>& v, const string& input) {
    string result = input; 
    bool modified = true; //прапорець для відстежування змін

    while (modified) {
        modified = false;

        for (int i = 0; i < u.size(); i++) { //ітерація по кожному правилу
            size_t pos = result.find(u[i]); //знаходимо перше співпадіння u[i] у результуючому рядку

            if (pos != string::npos) { //якщо знайдено співпадіння, то замінюємо знайдену підстроку на v[i]
                result.replace(pos, u[i].length(), v[i]); 
                modified = true; //встановлюємо прапорець замін, щоб позначити, що відбулася хоча б одна зміна
            }

            cout << result << endl; //виводимо проміжний результат
        }
    }

    return result;
}

int main() {
   
    vector<string> u = { "1", "|0", "0" };
    vector<string> v = { "0|", "0||", "" };

    string input = "111"; 
    string expected_output = "|||||||";

    string output = markov(u, v, input);

    cout << "Input: " << input << endl;
    cout << "Output: " << output << endl;
    cout << "Expected Output: " << expected_output << endl;

    return 0;
}
