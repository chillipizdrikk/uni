using System;
using System.Collections.Generic;
using System.Linq;

class Car
{
    public string Model { get; set; }
    public int Year { get; set; }
    public string Color { get; set; }
    public List<double> PriceHistory { get; } = new List<double>(); // Додайте поле для збереження історії цін

    public override string ToString()
    {
        return $"{Color} {Year} {Model}";
    }
}

class PricingInformation
{
    public double BasePrice { get; set; }
    public double Taxes { get; set; }
    public double Discount { get; set; }

    public double GetTotalPrice()
    {
        double totalPrice = BasePrice * (1 + Taxes / 100);
        totalPrice -= totalPrice * (Discount / 100);
        return totalPrice;
    }
}

class CarSystem
{
    private Dictionary<Car, PricingInformation> cars = new Dictionary<Car, PricingInformation>();

    public void DisplayAllCars()
    {
        if (cars.Count == 0)
        {
            Console.WriteLine("No cars available.");
            return;
        }
        foreach (var pair in cars)
        {
            Console.WriteLine($"{pair.Key}: {pair.Value.GetTotalPrice()}");
        }
    }

    public void DisplayCheapestCar()
    {
        if (cars.Count == 0)
        {
            Console.WriteLine("No cars available.");
            return;
        }
        var cheapestCar = cars.Keys.MinBy(car => cars[car].GetTotalPrice());
        Console.WriteLine($"Cheapest car: {cheapestCar}: {cars[cheapestCar].GetTotalPrice()}");
    }

    public void DisplayMostExpensiveCar()
    {
        if (cars.Count == 0)
        {
            Console.WriteLine("No cars available.");
            return;
        }
        var expensiveCar = cars.Keys.MaxBy(car => cars[car].GetTotalPrice());
        Console.WriteLine($"Most expensive car: {expensiveCar}: {cars[expensiveCar].GetTotalPrice()}");
    }

    public void DisplayOldestCar()
    {
        if (cars.Count == 0)
        {
            Console.WriteLine("No cars available.");
            return;
        }
        var oldestCar = cars.Keys.MinBy(car => car.Year);
        Console.WriteLine($"Oldest car: {oldestCar}");
    }

    public void DisplayNewestCar()
    {
        if (cars.Count == 0)
        {
            Console.WriteLine("No cars available.");
            return;
        }
        var newestCar = cars.Keys.MaxBy(car => car.Year);
        Console.WriteLine($"Newest car: {newestCar}");
    }

    public void AddCar(Car car, PricingInformation pricingInfo)
    {
        cars.Add(car, pricingInfo);
    }

    public void RemoveCar(Car car)
    {
        if (!cars.ContainsKey(car))
        {
            Console.WriteLine("Car not found in the system.");
            return;
        }
        cars.Remove(car);
        Console.WriteLine("Car removed successfully.");
    }

    public void ChangePrice(Car car, PricingInformation newPricingInfo)
    {
        var carToUpdate = cars.Keys.FirstOrDefault(c => c.Model == car.Model && c.Year == car.Year && c.Color == car.Color);
        if (carToUpdate != null)
        {
            cars[carToUpdate] = newPricingInfo;
            carToUpdate.PriceHistory.Add(newPricingInfo.GetTotalPrice());
            Console.WriteLine("Price changed successfully.");
        }
        else
        {
            Console.WriteLine("Car not found in the system.");
        }
    }

    public void DisplayPriceChangeHistory(Car car)
    {
        var carToDisplay = cars.Keys.FirstOrDefault(c =>
            c.Model == car.Model &&
            c.Year == car.Year &&
            c.Color == car.Color);

        if (carToDisplay != null)
        {
            Console.WriteLine($"Price change history for {carToDisplay.Color} {carToDisplay.Year} {carToDisplay.Model}:");
            foreach (var price in carToDisplay.PriceHistory)
            {
                Console.WriteLine($"- Price: {price:C}"); 
            }
        }
        else
        {
            Console.WriteLine("Car not found in the system.");
        }
    }


    public void DisplayCompanyIncome()
    {
        double totalIncome = cars.Values.Sum(pricingInfo => pricingInfo.GetTotalPrice());
        Console.WriteLine($"Total company income: {totalIncome}");
    }
}

class Program
{
    static void Main(string[] args)
    {
        CarSystem carSystem = new CarSystem();
        // Додавання деяких автомобілів для тестування
        carSystem.AddCar(new Car { Model = "Toyota", Year = 2020, Color = "Red" }, new PricingInformation { BasePrice = 25000, Taxes = 10, Discount = 5 });
        carSystem.AddCar(new Car { Model = "Honda", Year = 2019, Color = "Blue" }, new PricingInformation { BasePrice = 22000, Taxes = 8, Discount = 3 });
        carSystem.AddCar(new Car { Model = "Ford", Year = 2021, Color = "Black" }, new PricingInformation { BasePrice = 28000, Taxes = 12, Discount = 6 });

        while (true)
        {
            Console.WriteLine("\nMenu:");
            Console.WriteLine("a) Display information about all available cars");
            Console.WriteLine("b) Display the cheapest car");
            Console.WriteLine("c) Display the most expensive car");
            Console.WriteLine("d) Display the oldest car");
            Console.WriteLine("e) Display the newest car");
            Console.WriteLine("f) Add a new car to the system");
            Console.WriteLine("g) Remove a car from the system");
            Console.WriteLine("h) Change the price of a car");
            Console.WriteLine("i) Display price change history for a specific car");
            Console.WriteLine("j) Display the company's total income");
            Console.WriteLine("q) Quit");

            string choice = Console.ReadLine().ToLower();

            switch (choice)
            {
                case "a":
                    carSystem.DisplayAllCars();
                    break;
                case "b":
                    carSystem.DisplayCheapestCar();
                    break;
                case "c":
                    carSystem.DisplayMostExpensiveCar();
                    break;
                case "d":
                    carSystem.DisplayOldestCar();
                    break;
                case "e":
                    carSystem.DisplayNewestCar();
                    break;
                case "f":
                    Console.Write("Enter car model: ");
                    string model = Console.ReadLine();
                    Console.Write("Enter car year: ");
                    int year = int.Parse(Console.ReadLine());
                    Console.Write("Enter car color: ");
                    string color = Console.ReadLine();
                    Console.Write("Enter base price: ");
                    double basePrice = double.Parse(Console.ReadLine());
                    Console.Write("Enter taxes percentage: ");
                    double taxes = double.Parse(Console.ReadLine());
                    Console.Write("Enter discount percentage: ");
                    double discount = double.Parse(Console.ReadLine());
                    Car newCar = new Car { Model = model, Year = year, Color = color };
                    PricingInformation pricingInfo = new PricingInformation { BasePrice = basePrice, Taxes = taxes, Discount = discount };
                    carSystem.AddCar(newCar, pricingInfo);
                    Console.WriteLine("Car added successfully.");
                    break;
                case "g":
                    Console.Write("Enter car model: ");
                    string removeModel = Console.ReadLine();
                    Console.Write("Enter car year: ");
                    int removeYear = int.Parse(Console.ReadLine());
                    Console.Write("Enter car color: ");
                    string removeColor = Console.ReadLine();
                    Car removeCar = new Car { Model = removeModel, Year = removeYear, Color = removeColor };
                    carSystem.RemoveCar(removeCar);
                    break;
                case "h":
                    Console.Write("Enter car model: ");
                    string changeModel = Console.ReadLine();
                    Console.Write("Enter car year: ");
                    int changeYear = int.Parse(Console.ReadLine());
                    Console.Write("Enter car color: ");
                    string changeColor = Console.ReadLine();
                    Car changeCar = new Car { Model = changeModel, Year = changeYear, Color = changeColor };
                    Console.Write("Enter new base price: ");
                    double newBasePrice = double.Parse(Console.ReadLine());
                    Console.Write("Enter new taxes percentage: ");
                    double newTaxes = double.Parse(Console.ReadLine());
                    Console.Write("Enter new discount percentage: ");
                    double newDiscount = double.Parse(Console.ReadLine());
                    PricingInformation newPricingInfo = new PricingInformation { BasePrice = newBasePrice, Taxes = newTaxes, Discount = newDiscount };
                    carSystem.ChangePrice(changeCar, newPricingInfo);
                    break;
                case "i":
                    Console.Write("Enter car model: ");
                    string modelToDisplay = Console.ReadLine();
                    Console.Write("Enter car year: ");
                    int yearToDisplay = int.Parse(Console.ReadLine());
                    Console.Write("Enter car color: ");
                    string colorToDisplay = Console.ReadLine();
                    Car carToDisplay = new Car { Model = modelToDisplay, Year = yearToDisplay, Color = colorToDisplay };
                    carSystem.DisplayPriceChangeHistory(carToDisplay);
                    break;
                case "j":
                    carSystem.DisplayCompanyIncome();
                    break;
                case "q":
                    Environment.Exit(0);
                    break;
                default:
                    Console.WriteLine("Invalid choice. Please enter a valid option.");
                    break;
            }
        }
    }
}

