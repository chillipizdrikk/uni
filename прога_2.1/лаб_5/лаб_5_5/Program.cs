using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

// Базовий клас ресурсу
class Resource
{
    public decimal Price { get; set; }
    public string Origin { get; set; }

    public Resource(decimal price, string origin)
    {
        Price = price;
        Origin = origin;
    }
}

// Похідні класи ресурсів
class Gold : Resource
{
    public Gold(decimal price, string origin) : base(price, origin) { }
}

class Silver : Resource
{
    public Silver(decimal price, string origin) : base(price, origin) { }
}

class Coal : Resource
{
    public Coal(decimal price, string origin) : base(price, origin) { }
}

// Клас країни
class Country
{
    public event EventHandler<string> NewsEvent;

    public string Name { get; private set; }

    public Country(string name)
    {
        Name = name;
    }

    public void GenerateEvent(string eventName)
    {
        NewsEvent?.Invoke(this, eventName);
    }
}

class Program
{
    static Dictionary<string, Resource> resources = new Dictionary<string, Resource>();
    static Dictionary<string, Country> countries = new Dictionary<string, Country>();
    static Dictionary<string, List<string>> eventsHistory = new Dictionary<string, List<string>>();
    static Dictionary<string, List<decimal>> priceHistory = new Dictionary<string, List<decimal>>();

    static void Main(string[] args)
    {
        // Додати ресурси
        resources.Add("Gold", new Gold(1000, "USA"));
        resources.Add("Silver", new Silver(50, "Poland"));
        resources.Add("Coal", new Coal(200, "Canada"));
        resources.Add("Diamond", new Gold(5000, "South Africa"));
        resources.Add("Platinum", new Silver(150, "Ukraine"));

        // Додати країни
        countries.Add("USA", new Country("USA"));
        countries.Add("Poland", new Country("Poland"));
        countries.Add("Canada", new Country("Canada"));
        countries.Add("South Africa", new Country("South Africa"));
        countries.Add("Ukraine", new Country("Ukraine"));

        // Підписатись на новини з різних країн
        foreach (var country in countries.Values)
        {
            country.NewsEvent += HandleNewsEvent;
        }

        // Консольне меню
        while (true)
        {
            Console.OutputEncoding = Encoding.UTF8;

            Console.WriteLine("Меню:");
            Console.WriteLine("1. Вивести усі ресурси наявні в системі");
            Console.WriteLine("2. Згенерувати подію певного типу для певної країни");
            Console.WriteLine("3. Вивести країну, де можна найдешевше купити певний ресурс");
            Console.WriteLine("4. Вивести країну, де можна найдорожче купити певний ресурс");
            Console.WriteLine("5. Вивести історію змін ціни для певного ресурсу з певної країни");
            Console.WriteLine("6. Вивести події, що стались в країні від початку роботи програми");
            Console.WriteLine("7. Вийти з програми");

            Console.Write("Виберіть опцію: ");
            int choice;
            bool isValidChoice = int.TryParse(Console.ReadLine(), out choice);

            if (!isValidChoice)
            {
                Console.WriteLine("Невірний вибір. Спробуйте ще раз.");
                continue;
            }

            switch (choice)
            {
                case 1:
                    PrintAllResources();
                    break;
                case 2:
                    GenerateEvent();
                    break;
                case 3:
                    FindCheapestCountry();
                    break;
                case 4:
                    FindMostExpensiveCountry();
                    break;
                case 5:
                    PrintPriceHistory();
                    break;
                case 6:
                    PrintEventsHistory();
                    break;
                case 7:
                    Environment.Exit(0);
                    break;
                default:
                    Console.WriteLine("Невірний вибір. Спробуйте ще раз.");
                    break;
            }
        }
    }

    static void HandleNewsEvent(object sender, string eventName)
    {
        Country country = sender as Country;
        List<string> countryEvents;
        if (!eventsHistory.ContainsKey(country.Name))
        {
            countryEvents = new List<string>();
            eventsHistory.Add(country.Name, countryEvents);
        }
        else
        {
            countryEvents = eventsHistory[country.Name];
        }
        countryEvents.Add(eventName);

        switch (eventName)
        {
            case "Economic growth":
            case "Olympic Games":
                foreach (var resource in resources.Values)
                {
                    if (resource.Origin == country.Name)
                        resource.Price *= 1.1m;
                    else
                        resource.Price *= 0.95m;
                }
                break;
            case "Corruption":
            case "Disaster":
                foreach (var resource in resources.Values)
                {
                    if (resource.Origin == country.Name)
                        resource.Price *= 0.9m;
                    else
                        resource.Price *= 1.05m;
                }
                break;
        }

        // Оновлення історії змін цін
        foreach (var resource in resources.Values)
        {
            if (resource.Origin == country.Name)
            {
                if (!priceHistory.ContainsKey(resource.Origin))
                    priceHistory[resource.Origin] = new List<decimal>();
                priceHistory[resource.Origin].Add(resource.Price);
            }
        }

        Console.WriteLine($"Подія {eventName} сталася в країні {country.Name}");
    }

    static void PrintAllResources()
    {
        Console.WriteLine("Ресурси наявні в системі:");
        foreach (var resource in resources)
        {
            Console.WriteLine($"Назва: {resource.Key}, Ціна: {resource.Value.Price}, Місце видобутку: {resource.Value.Origin}");
        }
    }

    static void GenerateEvent()
    {
        Console.WriteLine("Введіть назву події (Corruption, Disaster, Economic growth, Olympic Games):");
        string eventName = Console.ReadLine();
        Console.WriteLine("Введіть назву країни (USA, Poland, Canada, South Africa, Ukraine):");
        string countryName = Console.ReadLine();

        // Перевірка правильності введених даних для країни та події
        if (!countries.ContainsKey(countryName))
        {
            Console.WriteLine("Невірна назва країни.");
            return;
        }

        // Видаляємо зайві пробіли з початку і кінця рядка
        eventName = eventName.Trim();

        // Шукаємо країну, ігноруючи регістр та можливі пробіли
        var foundCountry = countries[countryName];
        foundCountry.GenerateEvent(eventName);
    }

    static void FindCheapestCountry()
    {
        Console.WriteLine("Введіть назву ресурсу (Gold, Silver, Coal, Diamond, Platinum):");
        string resourceName = Console.ReadLine().Trim();

        decimal minPrice = decimal.MaxValue;
        string cheapestCountry = "";

        foreach (var resource in resources.Values)
        {
            if (resource.GetType().Name.Equals(resourceName, StringComparison.OrdinalIgnoreCase) && resource.Price < minPrice)
            {
                minPrice = resource.Price;
                cheapestCountry = resource.Origin;
            }
        }

        if (!string.IsNullOrEmpty(cheapestCountry))
        {
            Console.WriteLine($"Найдешевший ресурс {resourceName} доступний в країні {cheapestCountry} за ціною {minPrice}");
        }
        else
        {
            Console.WriteLine($"Ресурс {resourceName} не знайдений або немає інформації про його ціну в системі.");
        }
    }

    static void FindMostExpensiveCountry()
    {
        Console.WriteLine("Введіть назву ресурсу (Gold, Silver, Coal, Diamond, Platinum):");
        string resourceName = Console.ReadLine().Trim();

        decimal maxPrice = decimal.MinValue;
        string expensiveCountry = "";

        foreach (var resource in resources.Values)
        {
            if (resource.GetType().Name.Equals(resourceName, StringComparison.OrdinalIgnoreCase) && resource.Price > maxPrice)
            {
                maxPrice = resource.Price;
                expensiveCountry = resource.Origin;
            }
        }

        if (!string.IsNullOrEmpty(expensiveCountry))
        {
            Console.WriteLine($"Найдорожчий ресурс {resourceName} доступний в країні {expensiveCountry} за ціною {maxPrice}");
        }
        else
        {
            Console.WriteLine($"Ресурс {resourceName} не знайдений або немає інформації про його ціну в системі.");
        }
    }

    static void PrintPriceHistory()
    {
        Console.WriteLine("Введіть назву ресурсу (Gold, Silver, Coal, Diamond, Platinum):");
        string resourceName = Console.ReadLine().Trim();

        Console.WriteLine("Введіть назву країни (USA, Poland, Canada, South Africa, Ukraine):");
        string countryName = Console.ReadLine().Trim();

        if (priceHistory.ContainsKey(countryName) && resources.ContainsKey(resourceName))
        {
            Console.WriteLine($"Історія змін цін на ресурс {resourceName} у країні {countryName}:");
            foreach (var price in priceHistory[countryName])
            {
                Console.WriteLine($"Ціна: {price}");
            }
        }
        else
        {
            Console.WriteLine("Немає доступної історії для вказаного ресурсу або країни.");
        }
    }

    static void PrintEventsHistory()
    {
        Console.WriteLine("Введіть назву країни (USA, Poland, Canada, South Africa, Ukraine):");
        string countryName = Console.ReadLine().Trim();

        if (eventsHistory.ContainsKey(countryName))
        {
            Console.WriteLine($"Події, які сталися в країні {countryName} з моменту початку роботи програми:");
            foreach (var eventName in eventsHistory[countryName])
            {
                Console.WriteLine($"Подія: {eventName}");
            }
        }
        else
        {
            Console.WriteLine("Немає доступної історії подій для вказаної країни.");
        }
    }
}


