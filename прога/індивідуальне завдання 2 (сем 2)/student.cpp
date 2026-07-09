#include "student.h"
#include <iostream>
using namespace std;

Student::Student()
    : name_(""), surname_(""), group_("")
{}

Student::Student(const string& name, const string& surname, const string& group)
    : name_(name), surname_(surname), group_(group)
{}

Student::Student(const Student& s)
    : name_(s.name_), surname_(s.surname_), group_(s.group_), grade_(s.grade_)
{}

Student::~Student()
{}

void Student::PrintInfo() const {
    cout << "Student: " << name_ << " " << surname_ << "\n";
    cout << "Group: " << group_ << "\n";
    cout << "Grades in: " << "\n";
    for (const auto& grade : grade_) {
        std::string subject_name;
        switch (grade.first) {
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
        cout << subject_name << ": " << grade.second << "/100   ";
    }
    cout << "\n\n";
}

void Student::AddGrade(Subject subject, int grade) {
    grade_.push_back(make_pair(subject, grade));
}

int Student::GetGrade(Subject subject) const {
    for (const auto& grade : grade_) {
        if (grade.first == subject) {
            return grade.second;
        }
    }
    throw runtime_error("Error");
}

vector<pair<Subject, int>> Student::AllGrades() const {
    return grade_;
}

string Student::GetGroup() const {
    return group_;
}

void Student::ReadFrom(istream& in) {
    in >> name_ >> surname_ >> group_;
    string subject; int grade, n;
    in >> n;
    for (int i = 0; i < n; ++i) {
        in >> subject >> grade;
        Subject subject_enum;
        if (subject == "PE") {
            subject_enum = Subject::PE;
        }
        else if (subject == "Biology") {
            subject_enum = Subject::BIOLOGY;
        }
        else if (subject == "English") {
            subject_enum = Subject::ENGLISH;
        }
        grade_.push_back(make_pair(subject_enum, grade));
    }
}

void Student::WriteTo(ostream& out) const {
    out << name_ << " " << surname_ << " " << group_ << " | ";
    for (const auto& grade : grade_) {
        out << grade.first << " " << grade.second << " | ";
    }
}

istream& operator>> (istream& in, Student& s) {
    s.ReadFrom(in);
    return in;
}

ostream& operator<< (ostream& out, const Student& s) {
    s.WriteTo(out);
    return out;
}

ostream& operator<<(ostream& out, const Subject& S) {
    switch (S)
    {
    case Subject::PE:
        out << "PE";
        break;
    case Subject::BIOLOGY:
        out << "Biology";
        break;
    case Subject::ENGLISH:
        out << "English";
        break;
    }
    return out;
}

Student TheMostSuccessfulStudent(const vector<Student>& students, Subject subject) {
    Student top_student;
    int max_grade = 0;
    for (const auto& student : students) {
        int grade = student.GetGrade(subject);
        if (grade > max_grade) {
            max_grade = grade;
            top_student = student;
        }
    }
    return top_student;
}

map<string, float> TheMostSuccessfulGroup(const vector<Student>& students, Subject subject) {
    map<string, pair<int, int>> group_grades;
    for (const auto& student : students) {
        int grade = student.GetGrade(subject);
        group_grades[student.GetGroup()].first += grade;
        group_grades[student.GetGroup()].second++;
    }

    string top_group;
    float max_average_grade = 0.0;
    for (const auto& entry : group_grades) {
        float average_grade = static_cast<float>(entry.second.first) / entry.second.second;
        if (average_grade > max_average_grade) {
            max_average_grade = average_grade;
            top_group = entry.first;
        }
    }
    map<string, float> average_grades;
    average_grades[top_group] = max_average_grade;
    return average_grades;
}

map<Subject, int> Summary(const vector<Student>& students) {
    map<Subject, int> summary;
    for (const auto& student : students) {
        for (const auto& grade : student.AllGrades()) {
            summary[grade.first] += grade.second;
        }
    }
    return summary;
}