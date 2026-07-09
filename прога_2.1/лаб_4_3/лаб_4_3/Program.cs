using System;
using System.Collections.Generic;
using System.Transactions;

class Product
{
    public int Id { get; set; }
    public string Name { get; set; }
    public decimal Price { get; set; }
    public int Amount { get; set; }

    public Product(int id, string name, decimal price, int amount)
    {
        Id = id;
        Name = name;
        Price = price;
        Amount = amount;
    }
}

class Vegetable : Product
{
    public string Color { get; set; }

    public Vegetable(int id, string name, decimal price, int amount, string color)
        : base(id, name, price, amount)
    {
        Color = color;
    }
}

class DairyProduct : Product
{
    public DateTime ExpirationDate { get; set; }

    public DairyProduct(int id, string name, decimal price, int amount, DateTime expirationDate)
        : base(id, name, price, amount)
    {
        ExpirationDate = expirationDate;
    }
}

class Beverage : Product
{
    public bool IsCarbonated { get; set; }

    public Beverage(int id, string name, decimal price, int amount, bool isCarbonated)
        : base(id, name, price, amount)
    {
        IsCarbonated = isCarbonated;
    }
}
class Transaction
{
    public decimal Amount { get; set; }

    public Transaction(decimal amount)
    {
        Amount = amount;
    }
}

class Program
{
    static void Main()
    {
        var products = new List<Product>
        {
            new Vegetable(1, "Помiдор", 22, 10, "Червоний"),
            new DairyProduct(2, "Молоко", 40, 5, new DateTime(2024, 3, 31)),
            new Beverage(3, "Кола", 35, 20, true)
        };

        var transactions = new List<Transaction>();

        char choice;
        do
        {
            Console.WriteLine("Меню:");
            Console.WriteLine("a. Видрукувати всю продукцiю");
            Console.WriteLine("b. Видрукувати продукцiю за категорiєю");
            Console.WriteLine("c. Видрукувати тi продукти, цiна яких бiльша за N"); 
            Console.WriteLine("d. Видрукувати ті продукти, ціна яких менша за N");
            Console.WriteLine("e. Видрукувати ті продукти, кількість яких більша за N");
            Console.WriteLine("f. Видрукувати ті продукти, кількість яких менша за N");
            Console.WriteLine("g. Додати новий товар певного типу");
            Console.WriteLine("h. Додати декілька одиниць певного продукту(закупівля товару)");
            Console.WriteLine("i. Вилучити декілька одиниць певного продукту(продаж товару)");
            Console.WriteLine("j. Видрукувати загальну вартість усіх продуктів");
            Console.WriteLine("k. Видрукувати дохід з моменту запуску програми після додавання продуктів, закупівель і продажів");
            Console.WriteLine("l. Вийти з програми");
            Console.Write("Оберiть опцiю:");
            choice = Char.ToLower(Console.ReadKey().KeyChar);
            Console.WriteLine();

            switch (choice)
            {
                case 'a':
                    PrintAllProducts(products);
                    break;
                case 'b':
                    PrintProductsByCategory(products);
                    break;
                case 'c':
                    PrintProductsByPrice(products);
                    break;
                case 'd':
                    PrintProductsByPriceLessThanN(products);
                    break;
                case 'e':
                    PrintProductsByAmountGreaterThanN(products);
                    break;
                case 'f':
                    PrintProductsByAmountLessThanN(products);
                    break;
                case 'g':
                    AddNewProductOfType(products);
                    break;
                case 'h':
                    PurchaseProduct(products, transactions);
                    break;
                case 'i':
                    SellProduct(products, transactions);
                    break;
                case 'j':
                    PrintTotalValueOfProducts(products);
                    break;
                case 'k':
                    PrintTotalIncome(transactions);
                    break;
                case 'l':
                    Console.WriteLine("Дякую за використання програми. До побачення!");
                    break;
                default:
                    Console.WriteLine("Неправильний вибiр. Будь ласка, спробуйте ще раз.");
                    break;
            }

            Console.WriteLine();
        } while (choice != 'l');
    }

    static void PrintAllProducts(List<Product> products)
    {
        Console.WriteLine("Вся продукцiя:");
        foreach (var product in products)
        {
            Console.WriteLine($"ID: {product.Id}, Назва: {product.Name}, Цiна: {product.Price:C}, Кiлькiсть: {product.Amount}");
            if (product is Vegetable veggie)
                Console.WriteLine($"Колiр: {veggie.Color}");
            else if (product is DairyProduct dairy)
                Console.WriteLine($"Термiн придатностi: {dairy.ExpirationDate:d}");
            else if (product is Beverage beverage)
                Console.WriteLine($"Газований: {beverage.IsCarbonated}");
            Console.WriteLine();
        }
    }

    static void PrintProductsByCategory(List<Product> products)
    {
        Console.WriteLine("Оберiть категорiю продуктiв:");
        Console.WriteLine("1. Овочi");
        Console.WriteLine("2. Молочнi продукти");
        Console.WriteLine("3. Напої");

        Console.Write("Введiть номер категорiї: ");
        int categoryChoice;
        if (!int.TryParse(Console.ReadLine(), out categoryChoice) || categoryChoice < 1 || categoryChoice > 3)
        {
            Console.WriteLine("Невiрний ввiд. Будь ласка, введiть номер від 1 до 3.");
            return;
        }

        switch (categoryChoice)
        {
            case 1:
                PrintProductsByCategory(products, typeof(Vegetable));
                break;
            case 2:
                PrintProductsByCategory(products, typeof(DairyProduct));
                break;
            case 3:
                PrintProductsByCategory(products, typeof(Beverage));
                break;
        }
    }

    static void PrintProductsByCategory(List<Product> products, Type categoryType)
    {
        Console.WriteLine($"Продукти в категорiї \"{categoryType.Name}\":");
        foreach (var product in products)
        {
            if (product.GetType() == categoryType)
            {
                Console.WriteLine($"ID: {product.Id}, Назва: {product.Name}, Цiна: {product.Price:C}, Кiлькiсть: {product.Amount}");
                if (product is Vegetable veggie)
                    Console.WriteLine($"Колiр: {veggie.Color}");
                else if (product is DairyProduct dairy)
                    Console.WriteLine($"Термiн придатностi: {dairy.ExpirationDate:d}");
                else if (product is Beverage beverage)
                    Console.WriteLine($"Газований: {beverage.IsCarbonated}");
                Console.WriteLine();
            }
        }
    }

    static void PrintProductsByPrice(List<Product> products)
    {
        Console.Write("Введiть мiнiмальну цiну: ");
        decimal minPrice;
        if (!decimal.TryParse(Console.ReadLine(), out minPrice))
        {
            Console.WriteLine("Невiрний ввiд. Будь ласка, введiть дiйсне число.");
            return;
        }

        Console.WriteLine($"Продукти з цiною бiльшою за {minPrice:C}:");
        foreach (var product in products)
        {
            if (product.Price > minPrice)
            {
                Console.WriteLine($"ID: {product.Id}, Назва: {product.Name}, Цiна: {product.Price:C}, Кiлькiсть: {product.Amount}");
                if (product is Vegetable veggie)
                    Console.WriteLine($"Колiр: {veggie.Color}");
                else if (product is DairyProduct dairy)
                    Console.WriteLine($"Термiн придатностi: {dairy.ExpirationDate:d}");
                else if (product is Beverage beverage)
                    Console.WriteLine($"Газований: {beverage.IsCarbonated}");
                Console.WriteLine();
            }
        }
    }

    static void PrintProductsByPriceLessThanN(List<Product> products)
    {
        Console.Write("Введіть максимальну ціну: ");
        decimal maxPrice;
        if (!decimal.TryParse(Console.ReadLine(), out maxPrice))
        {
            Console.WriteLine("Невірний ввід. Будь ласка, введіть дійсне число.");
            return;
        }

        Console.WriteLine($"Продукти з ціною меншою за {maxPrice:C}:");
        foreach (var product in products)
        {
            if (product.Price < maxPrice)
            {
                PrintProductDetails(product);
            }
        }
    }

    static void PrintProductsByAmountGreaterThanN(List<Product> products)
    {
        Console.Write("Введіть мінімальну кількість: ");
        int minAmount;
        if (!int.TryParse(Console.ReadLine(), out minAmount))
        {
            Console.WriteLine("Невірний ввід. Будь ласка, введіть ціле число.");
            return;
        }

        Console.WriteLine($"Продукти з кількістю більшою за {minAmount}:");
        foreach (var product in products)
        {
            if (product.Amount > minAmount)
            {
                PrintProductDetails(product);
            }
        }
    }

    static void PrintProductsByAmountLessThanN(List<Product> products)
    {
        Console.Write("Введіть максимальну кількість: ");
        int maxAmount;
        if (!int.TryParse(Console.ReadLine(), out maxAmount))
        {
            Console.WriteLine("Невірний ввід. Будь ласка, введіть ціле число.");
            return;
        }

        Console.WriteLine($"Продукти з кількістю меншою за {maxAmount}:");
        foreach (var product in products)
        {
            if (product.Amount < maxAmount)
            {
                PrintProductDetails(product);
            }
        }
    }

    static void PrintProductDetails(Product product)
    {
        Console.WriteLine($"ID: {product.Id}, Назва: {product.Name}, Ціна: {product.Price:C}, Кількість: {product.Amount}");
        if (product is Vegetable veggie)
            Console.WriteLine($"Колір: {veggie.Color}");
        else if (product is DairyProduct dairy)
            Console.WriteLine($"Термін придатності: {dairy.ExpirationDate:d}");
        else if (product is Beverage beverage)
            Console.WriteLine($"Газований: {beverage.IsCarbonated}");
        Console.WriteLine();
    }
    static void AddNewProductOfType(List<Product> products)
    {
        Console.WriteLine("Оберіть тип нового товару:");
        Console.WriteLine("1. Овочі");
        Console.WriteLine("2. Молочні продукти");
        Console.WriteLine("3. Напої");

        Console.Write("Введіть номер типу: ");
        int typeChoice;
        if (!int.TryParse(Console.ReadLine(), out typeChoice) || typeChoice < 1 || typeChoice > 3)
        {
            Console.WriteLine("Невірний ввід. Будь ласка, введіть номер від 1 до 3.");
            return;
        }

        Console.Write("Введіть назву нового товару: ");
        string name = Console.ReadLine();

        Console.Write("Введіть ціну нового товару: ");
        decimal price;
        if (!decimal.TryParse(Console.ReadLine(), out price))
        {
            Console.WriteLine("Невірний ввід. Будь ласка, введіть дійсне число.");
            return;
        }

        Console.Write("Введіть кількість нового товару: ");
        int amount;
        if (!int.TryParse(Console.ReadLine(), out amount))
        {
            Console.WriteLine("Невірний ввід. Будь ласка, введіть ціле число.");
            return;
        }

        switch (typeChoice)
        {
            case 1:
                Console.Write("Введіть колір овоча: ");
                string color = Console.ReadLine();
                products.Add(new Vegetable(products.Count + 1, name, price, amount, color));
                break;
            case 2:
                Console.Write("Введіть термін придатності: ");
                DateTime expirationDate;
                if (!DateTime.TryParse(Console.ReadLine(), out expirationDate))
                {
                    Console.WriteLine("Невірний ввід. Будь ласка, введіть дату в форматі yyyy-MM-dd.");
                    return;
                }
                products.Add(new DairyProduct(products.Count + 1, name, price, amount, expirationDate));
                break;
            case 3:
                Console.Write("Чи газований напій (true/false): ");
                bool isCarbonated;
                if (!bool.TryParse(Console.ReadLine(), out isCarbonated))
                {
                    Console.WriteLine("Невірний ввід. Будь ласка, введіть true або false.");
                    return;
                }
                products.Add(new Beverage(products.Count + 1, name, price, amount, isCarbonated));
                break;
        }

        Console.WriteLine("Новий товар успішно додано!");
    }

    static void PurchaseProduct(List<Product> products, List<Transaction> transactions)
    {
        Console.Write("Введіть ID продукту, який ви хочете придбати: ");
        int productId;
        if (!int.TryParse(Console.ReadLine(), out productId))
        {
            Console.WriteLine("Невірний ввід. Будь ласка, введіть ціле число.");
            return;
        }

        Console.Write("Введіть кількість одиниць товару: ");
        int amount;
        if (!int.TryParse(Console.ReadLine(), out amount))
        {
            Console.WriteLine("Невірний ввід. Будь ласка, введіть ціле число.");
            return;
        }

        Product product = products.Find(p => p.Id == productId);
        if (product == null)
        {
            Console.WriteLine("Продукт з введеним ID не знайдено.");
            return;
        }

        product.Amount += amount;
        transactions.Add(new Transaction(product.Price * amount));
        Console.WriteLine($"Куплено {amount} одиниць продукту \"{product.Name}\". Нова кількість: {product.Amount}");
    }

    static void SellProduct(List<Product> products, List<Transaction> transactions)
    {
        Console.Write("Введіть ID продукту, який ви хочете продати: ");
        int productId;
        if (!int.TryParse(Console.ReadLine(), out productId))
        {
            Console.WriteLine("Невірний ввід. Будь ласка, введіть ціле число.");
            return;
        }

        Console.Write("Введіть кількість одиниць товару: ");
        int amount;
        if (!int.TryParse(Console.ReadLine(), out amount))
        {
            Console.WriteLine("Невірний ввід. Будь ласка, введіть ціле число.");
            return;
        }

        Product product = products.Find(p => p.Id == productId);
        if (product == null)
        {
            Console.WriteLine("Продукт з введеним ID не знайдено.");
            return;
        }

        if (product.Amount < amount)
        {
            Console.WriteLine($"Недостатня кількість продукту \"{product.Name}\" для продажу.");
            return;
        }

        product.Amount -= amount;
        transactions.Add(new Transaction(product.Price * amount * -1));
        Console.WriteLine($"Продано {amount} одиниць продукту \"{product.Name}\". Нова кількість: {product.Amount}");
    }
    static void PrintTotalValueOfProducts(List<Product> products)
    {
        decimal totalValue = 0;
        foreach (var product in products)
        {
            totalValue += product.Price * product.Amount;
        }
        Console.WriteLine($"Загальна вартість усіх продуктів: {totalValue:C}");
    }

    static void PrintTotalIncome(List<Transaction> transactions)
    {
        decimal totalIncome = 0;
        foreach (var transaction in transactions)
        {
            totalIncome += transaction.Amount;
        }
        Console.WriteLine($"Дохід з моменту запуску програми: {totalIncome:C}");
    }


}
