//  - Простий приклад для Task 3 (дочірній процес на C++).
//  - Зчитує з файлу comdata.txt перший рядок як послідовність цілих чисел,
//    множить кожне число на 10 і записує результат назад у comdata.txt.
//  - Друкує проміжні повідомлення на консоль для протоколу.
// Виклик з Python (у task3_wait_main.py замініть виклик на subprocess.run(["task3_cpp_child.exe"]))

#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <string>

int main() {
    const std::string fn = "comdata.txt";
    std::cout << "task3_cpp_child.exe - початок виконання (C++ дочірній процес)\n";
    std::ifstream in(fn);
    if (!in) {
        std::cerr << "Помилка: не вдалося відкрити файл для читання: " << fn << "\n";
        return 1;
    }
    std::string line;
    if (!std::getline(in, line)) {
        std::cerr << "Файл порожній або не вдалось прочитати рядок.\n";
        return 1;
    }
    in.close();

    std::istringstream iss(line);
    std::vector<int> data;
    int x;
    while (iss >> x) data.push_back(x);

    std::cout << "Прочитані дані: ";
    for (int v : data) std::cout << v << " ";
    std::cout << "\n";

    for (int &v : data) v *= 10;

    std::cout << "Після множення на 10: ";
    for (int v : data) std::cout << v << " ";
    std::cout << "\n";

    std::ofstream out(fn);
    if (!out) {
        std::cerr << "Помилка: не вдалося відкрити файл для запису: " << fn << "\n";
        return 1;
    }
    for (size_t i = 0; i < data.size(); ++i) {
        if (i) out << " ";
        out << data[i];
    }
    out << "\n";
    out.close();

    std::cout << "Дані записані назад у файл: " << fn << "\n";
    std::cout << "task3_cpp_child.exe - кінець виконання. Натисніть Enter для завершення (якщо запущено вручну)...\n";
    // Якщо запущено з консолі, збережемо паузу, щоб було видно вивід
    std::cin.get();
    return 0;
}