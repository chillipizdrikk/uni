import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Завдання 1: Обчислення вектора з максимуму суми цифр елементів рядків матриці
        System.out.println("-----Завдання №1-----");

        // Введення розмірів матриці
        System.out.print("Введіть кількість рядків матриці: ");
        int rows = scanner.nextInt();
        System.out.print("Введіть кількість стовпців матриці: ");
        int cols = scanner.nextInt();

        int[][] matrix = new int[rows][cols];

        // Введення елементів матриці
        System.out.println("Введіть елементи матриці:");
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                matrix[i][j] = scanner.nextInt();
            }
        }

        // Обчислення вектора
        int[] resultVector = new int[rows];
        for (int i = 0; i < rows; i++) {
            int maxSumDigits = 0;
            for (int j = 0; j < cols; j++) {
                int sumDigits = sumOfDigits(matrix[i][j]);
                if (sumDigits > maxSumDigits) {
                    maxSumDigits = sumDigits;
                }
            }
            resultVector[i] = maxSumDigits;
        }

        // Виведення результату
        System.out.println("Результуючий вектор:");
        for (int value : resultVector) {
            System.out.print(value + " ");
        }

        // Завдання 2: Перетворення слів
        System.out.println("\n-----Завдання №2-----");

        // Введення послідовності слів
        System.out.print("Введіть послідовність слів, розділених комами: ");
        scanner.nextLine(); // Очистка буфера
        String input = scanner.nextLine();

        // Розділення слів та перетворення
        String[] words = input.split(",");
        for (int i = 0; i < words.length; i++) {
            words[i] = words[i].replace("g", "th");
        }

        // Виведення результату
        System.out.println("Перетворені слова:");
        for (String word : words) {
            System.out.print(word.trim() + " ");
        }

        // Завдання 3: Навчальні заклади
        System.out.println("\n-----Завдання №3-----");

        // Створення масиву навчальних закладів
        List<EducationalInstitution> institutions = new ArrayList<>();
        institutions.add(new School("Школа №93", "вул. Червоної Калини 5", 1975, 1, 500));
        institutions.add(new School("Школа №42", "вул. Пасічна 8", 1990, 2, 350));
        institutions.add(new School("Школа №13", "вул. Драгана 15", 1980, 3, 400));
        institutions.add(new University("Університет А", "вул. Б.Хмельницького 9", 1965, "IV", 10));
        institutions.add(new University("Університет Б", "вул. Стрийська 6", 1985, "III", 8));
        institutions.add(new University("Університет В", "вул. Наукова 17", 1970, "II", 8));

        // Сортування за роком заснування
        Collections.sort(institutions, Comparator.comparingInt(EducationalInstitution::getYearOfEstablishment));
        System.out.println("+Навчальні заклади, відсортовані за роком заснування:");
        for (EducationalInstitution institution : institutions) {
            System.out.println(institution);
        }

        // Знаходження школи з мінімальною кількістю учнів
        School minStudentsSchool = institutions.stream()
                .filter(School.class::isInstance)
                .map(School.class::cast)
                .min(Comparator.comparingInt(School::getNumberOfStudents))
                .orElse(null);
        System.out.println("\n+Школа з мінімальною кількістю учнів: \n" + minStudentsSchool);

        // Виведення ВУЗів вказаного рівня акредитації
        String accreditationLevel = "IV";
        System.out.println("\n+ВУЗи з рівнем акредитації " + accreditationLevel + ":");
        institutions.stream()
                .filter(University.class::isInstance)
                .map(University.class::cast)
                .filter(university -> university.getAccreditationLevel().equals(accreditationLevel))
                .forEach(System.out::println);
    }

    // Метод для обчислення суми цифр числа
    private static int sumOfDigits(int number) {
        int sum = 0;
        while (number != 0) {
            sum += number % 10;
            number /= 10;
        }
        return sum;
    }
}

// Абстрактний клас навчальний заклад
abstract class EducationalInstitution {
    private String name;
    private String address;
    private int yearOfEstablishment;

    public EducationalInstitution(String name, String address, int yearOfEstablishment) {
        this.name = name;
        this.address = address;
        this.yearOfEstablishment = yearOfEstablishment;
    }

    public int getYearOfEstablishment() {
        return yearOfEstablishment;
    }

    @Override
    public String toString() {
        return name + " (" + address + ", " + yearOfEstablishment + ")";
    }
}

// Клас СШ (школа)
class School extends EducationalInstitution {
    private int number;
    private int numberOfStudents;

    public School(String name, String address, int yearOfEstablishment, int number, int numberOfStudents) {
        super(name, address, yearOfEstablishment);
        this.number = number;
        this.numberOfStudents = numberOfStudents;
    }

    public int getNumberOfStudents() {
        return numberOfStudents;
    }

    @Override
    public String toString() {
        return super.toString() + " - Школа №" + number + " (Кількість учнів: " + numberOfStudents + ")";
    }
}

// Клас ВУЗ (університет)
class University extends EducationalInstitution {
    private String accreditationLevel;
    private int numberOfFaculties;

    public University(String name, String address, int yearOfEstablishment, String accreditationLevel, int numberOfFaculties) {
        super(name, address, yearOfEstablishment);
        this.accreditationLevel = accreditationLevel;
        this.numberOfFaculties = numberOfFaculties;
    }

    public String getAccreditationLevel() {
        return accreditationLevel;
    }

    @Override
    public String toString() {
        return super.toString() + " - Університет (Рівень акредитації: " + accreditationLevel + ", Кількість факультетів: " + numberOfFaculties + ")";
    }
}
