#pragma once
#include <string>
#include <vector>
#include <map>

using namespace std;

enum class Subject {
	PE,
	BIOLOGY,
	ENGLISH
};

class Student {
private:
	string name_;
	string surname_;
	string group_;
	vector<pair<Subject, int>> grade_;

public:
	Student();
	Student(const string& name, const string& surname, const string& group);
	Student(const Student& s);
	~Student();

	void PrintInfo() const;
	void AddGrade(Subject subject, int grade);
	int GetGrade(Subject subject) const;
	vector<pair<Subject, int>> AllGrades() const;
	string GetGroup() const;

	void ReadFrom(istream& in);
	void WriteTo(ostream& out) const;
};

istream& operator>> (istream& in, Student& s);
ostream& operator<< (ostream& out, const Student& s);

ostream& operator<<(ostream& out, const Subject& S);

Student TheMostSuccessfulStudent(const vector<Student>& students, Subject subject);
map<string, float> TheMostSuccessfulGroup(const vector<Student>& students, Subject subject);
map<Subject, int> Summary(const vector<Student>& students);
