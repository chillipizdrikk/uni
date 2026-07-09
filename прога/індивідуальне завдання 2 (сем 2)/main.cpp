#include <iostream>
#include <vector>
#include <fstream>
#include <map>
#include "student.h"
using namespace std;

int main() {

    vector<Student> students;
    ifstream iFile("students.txt");
    while (!iFile.eof()) {
        Student s;
        iFile >> s;
        students.push_back(s);
    }
    iFile.close();

    map<Subject, int> total_grades = Summary(students);
    cout << "Summary of all grades in:" << "\n";
    for (const auto& entry : total_grades) {
        string subject_name;
        switch (entry.first) {
        case Subject::PE:
            subject_name = "PE";
            break;
        case Subject::BIOLOGY:
            subject_name = "Biology";
            break;
        case Subject::ENGLISH:
            subject_name = "English";
            break;
        }
        cout << subject_name << ": " << entry.second << "\n";
    }
    cout << "\n----------ALL STUDENTS----------" << "\n\n";
    for (size_t i = 0; i < students.size(); ++i) {
        students[i].PrintInfo();
    }
    cout << "----------------------------------------------" << "\n\n";
    
    Student top_student1 = TheMostSuccessfulStudent(students, Subject::PE);
    cout << "The most successful student in PE: \n" << top_student1 << "\n\n";

    Student top_student2 = TheMostSuccessfulStudent(students, Subject::BIOLOGY);
    cout << "The most successful student in Biology: \n" << top_student2 << "\n\n";

    Student top_student3 = TheMostSuccessfulStudent(students, Subject::ENGLISH);
    cout << "The most successful student in English: \n" << top_student3 << "\n\n";
    cout << "----------------------------------------------" << "\n\n";

    cout << "The most successful group in PE: \n";
    map<std::string, float> top_group1 = TheMostSuccessfulGroup(students, Subject::PE);
    for (const auto& pair : top_group1) {
        cout << pair.first << ": " << pair.second << "\n";
    }
    cout << "\n";

    cout << "The most successful group in Biology: \n";
    map<std::string, float> top_group2 = TheMostSuccessfulGroup(students, Subject::BIOLOGY);
    for (const auto& pair : top_group2) {
        cout << pair.first << ": " << pair.second << "\n";
    }
    cout << "\n";

    cout << "The most successful group in English: \n";
    map<std::string, float> top_group3 = TheMostSuccessfulGroup(students, Subject::ENGLISH);
    for (const auto& pair : top_group3) {
        cout << pair.first << ": " << pair.second << "\n";
    }
    cout << "\n";

    return 0;
}