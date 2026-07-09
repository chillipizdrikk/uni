using System;
using System.Collections.Generic;

// Клас користувачів
public class User
{
    public int Id { get; set; }
    public string FirstName { get; set; }
    public string LastName { get; set; }
    public string Email { get; set; }
    public string Phone { get; set; }
}

// Клас товарів
public class Product
{
    public int Id { get; set; }
    public int CategoryId { get; set; }
    public string Model { get; set; }
    public int Year { get; set; }
    public decimal Price { get; set; }
    public string Color { get; set; }
}

// Клас категорій
public class Category
{
    public int Id { get; set; }
    public string Name { get; set; }
}

// Клас замовлень
public class Order
{
    public int Id { get; set; }
    public DateTime CreatedDate { get; set; }
    public decimal TotalPrice { get; set; }
    public string Status { get; set; }
    public int UserId { get; set; }
    public string Address { get; set; }
}

// Клас деталей замовлення
public class OrderDetail
{
    public int Id { get; set; }
    public int OrderId { get; set; }
    public int ProductId { get; set; }
    public int Quantity { get; set; }
    public decimal Price { get; set; }
}

class Program
{
    static List<User> users = new List<User>
        {
            new User { Id = 1, FirstName = "John", LastName = "Doe", Email = "john.doe@example.com", Phone = "123456789" },
            new User { Id = 2, FirstName = "Alice", LastName = "Smith", Email = "alice.smith@example.com", Phone = "987654321" },
            new User { Id = 3, FirstName = "Bob", LastName = "Johnson", Email = "bob.johnson@example.com", Phone = "456789123" }
        };

    static List<Category> categories = new List<Category>
        {
            new Category { Id = 1, Name = "Smartphones" },
            new Category { Id = 2, Name = "Laptops" },
            new Category { Id = 3, Name = "Tablets" }
        };

    static List<Product> products = new List<Product>
        {
            new Product { Id = 1, CategoryId = 1, Model = "iPhone 12", Year = 2020, Price = 1000, Color = "Black" },
            new Product { Id = 2, CategoryId = 1, Model = "Samsung Galaxy S21", Year = 2021, Price = 900, Color = "Blue" },
            new Product { Id = 3, CategoryId = 2, Model = "MacBook Pro", Year = 2021, Price = 2000, Color = "Silver" },
            new Product { Id = 4, CategoryId = 1, Model = "Samsung Galaxy S20", Year = 2021, Price = 899, Color = "White" },
            new Product { Id = 9, CategoryId = 2, Model = "Dell XPS 13", Year = 2021, Price = 1200, Color = "White" },
            new Product { Id = 10, CategoryId = 3, Model = "Lenovo ThinkPad", Year = 2021, Price = 1600, Color = "Gray" },
            new Product { Id = 11, CategoryId = 2, Model = "Acer Aspire 5", Year = 2020, Price = 600, Color = "Silver" },
            new Product { Id = 12, CategoryId = 3, Model = "ASUS ROG Strix", Year = 2021, Price = 1700, Color = "Black" },
            new Product { Id = 13, CategoryId = 2, Model = "Microsoft Surface Laptop 4", Year = 2021, Price = 1500, Color = "Blue" },
            new Product { Id = 15, CategoryId = 3, Model = "iPad Pro", Year = 2020, Price = 700, Color = "Just Black" },
            new Product { Id = 16, CategoryId = 1, Model = "OnePlus 9 Pro", Year = 2021, Price = 1200, Color = "Morning Mist" }
        };

            static List<Order> orders = new List<Order>
        {
            new Order { Id = 1, CreatedDate = DateTime.Now, TotalPrice = 1000, Status = "New", UserId = 1, Address = "123 Main St" },
            new Order { Id = 2, CreatedDate = DateTime.Now.AddDays(-1), TotalPrice = 2000, Status = "Paid", UserId = 2, Address = "456 Oak St" },
            new Order { Id = 3, CreatedDate = DateTime.Now.AddDays(-1), TotalPrice = 1500, Status = "Paid", UserId = 2, Address = "456 Oak St" },
            new Order { Id = 4, CreatedDate = DateTime.Now.AddDays(-1), TotalPrice = 3000, Status = "Paid", UserId = 2, Address = "456 Oak St" },
            new Order { Id = 5, CreatedDate = DateTime.Now.AddDays(-2), TotalPrice = 2500, Status = "Delivered", UserId = 1, Address = "789 Elm St" }
        };
        
        
        
            static List<OrderDetail> orderDetails = new List<OrderDetail>
        {
            new OrderDetail { Id = 1, OrderId = 1, ProductId = 1, Quantity = 1, Price = 1000 },
            new OrderDetail { Id = 2, OrderId = 2, ProductId = 2, Quantity = 2, Price = 1800 },
            new OrderDetail { Id = 3, OrderId = 3, ProductId = 3, Quantity = 1, Price = 1500 },
        
        };

    static void Main(string[] args)
    {
        PopulateTestData(); // Заповнення прикладових даних

        while (true)
        {
            Console.WriteLine("Консольне меню:");
            Console.WriteLine("a) Додати продукт в систему");
            Console.WriteLine("b) Додати замовлення в систему");
            Console.WriteLine("c) Оновити статус замовлення");
            Console.WriteLine("d) Вивести усі продукти за певною категорією");
            Console.WriteLine("e) Знайти постійних клієнтів");
            Console.WriteLine("f) Знайти дохід магазину за певний період часу");
            Console.WriteLine("g) Знайти топ 5 продуктів, які найкраще продаються");
            Console.WriteLine("h) Знайти дні тижня, коли найчастіше робляться покупки");
            Console.WriteLine("i) Знайти категорію, яка містить найбільшу середню вартість товару");
            Console.WriteLine("j) Знайти користувачів, які не робили замовлень або не оплатили їх");
            Console.WriteLine("k) Знайти користувачів, які в загальному зробили замовлень на суму більшу ніж середня сума усіх замовлень");
            Console.WriteLine("l) Вийти з програми");

            Console.Write("Виберіть опцію: ");
            string option = Console.ReadLine();

            switch (option.ToLower())
            {
                case "a":
                    AddProduct();
                    break;
                case "b":
                    AddOrder();
                    break;
                case "c":
                    UpdateOrderStatus();
                    break;
                case "d":
                    PrintProductsByCategory();
                    break;
                case "e":
                    FindRegularCustomers();
                    break;
                case "f":
                    CalculateRevenue();
                    break;
                case "g":
                    TopSellingProducts();
                    break;
                case "h":
                    BusiestShoppingDays();
                    break;
                case "i":
                    CategoryWithHighestAveragePrice();
                    break;
                case "j":
                    CustomersWithNoOrdersOrUnpaidOrders();
                    break;
                case "k":
                    CustomersWithTotalOrderAmountAboveAverage();
                    break;
                case "l":
                    return;
                default:
                    Console.WriteLine("Невірний вибір. Спробуйте ще раз.");
                    break;
            }

            Console.WriteLine();
        }
    }

    static void AddProduct()
    {
        Console.WriteLine("Додавання продукту:");

        // Запитати користувача про дані для нового продукту
        Console.Write("Введіть назву моделі продукту: ");
        string model = Console.ReadLine();

        Console.Write("Введіть ID категорії: ");
        int categoryId = int.Parse(Console.ReadLine());

        Console.Write("Введіть рік випуску: ");
        int year = int.Parse(Console.ReadLine());

        Console.Write("Введіть ціну: ");
        decimal price = decimal.Parse(Console.ReadLine());

        Console.Write("Введіть колір: ");
        string color = Console.ReadLine();

        // Створити новий об'єкт продукту з отриманими даними
        Product newProduct = new Product
        {
            Id = products.Count + 1, // Новий ID буде на 1 більший за останній
            CategoryId = categoryId,
            Model = model,
            Year = year,
            Price = price,
            Color = color
        };

        // Додати новий продукт до списку products
        products.Add(newProduct);

        Console.WriteLine("Продукт успішно додано до системи.");
    }


    static void AddOrder()
    {
        Console.WriteLine("Додавання замовлення:");

        // Запитати користувача про дані для нового замовлення
        Console.Write("Введіть ID користувача: ");
        int userId = int.Parse(Console.ReadLine());

        Console.Write("Введіть адресу доставки: ");
        string address = Console.ReadLine();

        Console.WriteLine("Список доступних продуктів:");
        foreach (var product in products)
        {
            Console.WriteLine($"ID: {product.Id}, Модель: {product.Model}, Ціна: {product.Price}");
        }

        Console.Write("Введіть ID продукту для замовлення (або 0 для завершення): ");
        int productId = int.Parse(Console.ReadLine());

        List<OrderDetail> orderDetails = new List<OrderDetail>();

        while (productId != 0)
        {
            Console.Write("Введіть кількість: ");
            int quantity = int.Parse(Console.ReadLine());

            // Знайти об'єкт продукту за ID
            Product productToAdd = products.FirstOrDefault(p => p.Id == productId);

            if (productToAdd != null)
            {
                // Додати деталі замовлення для цього продукту
                OrderDetail orderDetail = new OrderDetail
                {
                    ProductId = productId,
                    Quantity = quantity,
                    Price = productToAdd.Price * quantity
                };
                orderDetails.Add(orderDetail);
            }
            else
            {
                Console.WriteLine("Продукт з вказаним ID не знайдено.");
            }

            Console.Write("Введіть ID продукту для замовлення (або 0 для завершення): ");
            productId = int.Parse(Console.ReadLine());
        }

        // Обчислення TotalPrice за допомогою LINQ
        decimal totalPrice = orderDetails.Sum(od => od.Price);

        // Створити новий об'єкт замовлення
        Order newOrder = new Order
        {
            Id = orders.Count + 1,
            CreatedDate = DateTime.Now,
            TotalPrice = totalPrice,
            Status = "New",
            UserId = userId,
            Address = address
        };

        // Додати нове замовлення до списку orders
        orders.Add(newOrder);

        Console.WriteLine("Замовлення успішно додано до системи.");


        // Додати деталі замовлення до списку orderDetails
        List<OrderDetail> newOrderDetails = new List<OrderDetail>();
        foreach (var orderDetail in orderDetails)
        {
            orderDetail.OrderId = newOrder.Id;
            newOrderDetails.Add(orderDetail);
        }

        // Додати нові деталі замовлення до оригінальної колекції orderDetails
        orderDetails.AddRange(newOrderDetails);

    }


    static void UpdateOrderStatus()
    {
        Console.WriteLine("Оновлення статусу замовлення:");

        // Запитати користувача про ID замовлення для оновлення
        Console.Write("Введіть ID замовлення: ");
        int orderId = int.Parse(Console.ReadLine());

        // Знайти замовлення в списку orders за ID
        Order orderToUpdate = orders.Find(order => order.Id == orderId);

        if (orderToUpdate != null)
        {
            // Запитати користувача про новий статус замовлення
            Console.Write("Введіть новий статус замовлення: ");
            string newStatus = Console.ReadLine();

            // Оновити статус замовлення
            orderToUpdate.Status = newStatus;

            Console.WriteLine("Статус замовлення успішно оновлено.");
        }
        else
        {
            Console.WriteLine("Замовлення з таким ID не знайдено.");
        }
    }


    static void PrintProductsByCategory()
    {
        Console.WriteLine("Виведення продуктів за категорією:");

        // Виведення доступних категорій
        Console.WriteLine("Доступні категорії:");
        foreach (var category in categories)
        {
            Console.WriteLine($"{category.Id}. {category.Name}");
        }

        // Запитати користувача про ID категорії
        Console.Write("Введіть ID категорії для виведення продуктів: ");
        int categoryId = int.Parse(Console.ReadLine());

        // Знайти продукти за вказаною категорією
        var productsInCategory = products.Where(p => p.CategoryId == categoryId);

        // Виведення знайдених продуктів
        if (productsInCategory.Any())
        {
            Console.WriteLine($"Продукти в категорії \"{categories.FirstOrDefault(c => c.Id == categoryId)?.Name}\":");
            foreach (var product in productsInCategory)
            {
                Console.WriteLine($"ID: {product.Id}, Модель: {product.Model}, Рік: {product.Year}, Ціна: {product.Price}, Колір: {product.Color}");
            }
        }
        else
        {
            Console.WriteLine("Продукти вказаної категорії не знайдено.");
        }
    }

   
    static void FindRegularCustomers()
    {
        Console.WriteLine("Пошук постійних клієнтів:");

        // Групування замовлень за користувачами та підрахунок кількості оплачених замовлень для кожного користувача
        var paidOrdersCountByUser = from order in orders
                                    where order.Status == "Paid"
                                    group order by order.UserId into g
                                    where g.Count() >= 3
                                    select new
                                    {
                                        UserId = g.Key,
                                        PaidOrdersCount = g.Count()
                                    };

        // Вивести інформацію про постійних клієнтів
        if (paidOrdersCountByUser.Any())
        {
            Console.WriteLine("Постійні клієнти (з трьома або більше оплаченими замовленнями):");
            foreach (var user in paidOrdersCountByUser)
            {
                Console.WriteLine($"ID користувача: {user.UserId}, Кількість оплачених замовлень: {user.PaidOrdersCount}");
            }
        }
        else
        {
            Console.WriteLine("Постійні клієнти не знайдено.");
        }
    }

    static void CalculateRevenue()
    {
        Console.WriteLine("Розрахунок доходу магазину за певний період часу:");

        // Запитати користувача про період
        Console.Write("Введіть початкову дату у форматі yyyy-MM-dd: ");
        DateTime startDate = DateTime.Parse(Console.ReadLine());

        Console.Write("Введіть кінцеву дату у форматі yyyy-MM-dd: ");
        DateTime endDate = DateTime.Parse(Console.ReadLine());

        // Знайти всі замовлення, що потрапляють у вказаний період
        var ordersInPeriod = orders.Where(o => o.CreatedDate >= startDate && o.CreatedDate <= endDate);

        // Обчислити загальний дохід за вказаний період
        decimal totalRevenue = 0;
        foreach (var order in ordersInPeriod)
        {
            // Перевірити статус замовлення на момент обчислення доходу
            if (order.Status == "Paid" || order.Status == "Delivered")
            {
                totalRevenue += order.TotalPrice;
            }
        }

        // Вивести результат
        Console.WriteLine($"Загальний дохід магазину з {startDate.ToShortDateString()} по {endDate.ToShortDateString()}: {totalRevenue}");
    }



    static void TopSellingProducts()
    {
        Console.WriteLine("Знаходження топ 5 продуктів, які найкраще продаються:");

        // Групування деталей замовлень за ID продукту та підрахунок кількості проданих одиниць кожного продукту
        var soldProducts = from detail in orderDetails
                           group detail by detail.ProductId into g
                           select new
                           {
                               ProductId = g.Key,
                               TotalQuantity = g.Sum(d => d.Quantity)
                           };

        // Вибір топ 5 продуктів, які найкраще продаються
        var topProducts = soldProducts.OrderByDescending(p => p.TotalQuantity).Take(5);

        // Виведення результатів
        Console.WriteLine("Топ 5 продуктів, які найкраще продаються:");
        foreach (var product in topProducts)
        {
            var productName = products.FirstOrDefault(p => p.Id == product.ProductId)?.Model;
            Console.WriteLine($"Назва продукту: {productName}, Кількість проданих одиниць: {product.TotalQuantity}");
        }
    }


    static void BusiestShoppingDays()
    {
        Console.WriteLine("Знаходження найбільш активних днів для покупок:");

        // Групування замовлень за днем тижня та підрахунок кількості замовлень для кожного дня
        var shoppingDays = from order in orders
                           group order by order.CreatedDate.DayOfWeek into g
                           orderby g.Count() descending
                           select new
                           {
                               DayOfWeek = g.Key,
                               OrderCount = g.Count()
                           };

        // Виведення результатів
        Console.WriteLine("Найбільш активні дні для покупок:");
        foreach (var day in shoppingDays)
        {
            Console.WriteLine($"День тижня: {day.DayOfWeek}, Кількість замовлень: {day.OrderCount}");
        }
    }


    static void CategoryWithHighestAveragePrice()
    {
        Console.WriteLine("Знаходження категорії з найбільшою середньою вартістю товару:");

        // Групування продуктів за категорією та обчислення середньої вартості для кожної категорії
        var categoryAveragePrices = from product in products
                                    group product by product.CategoryId into g
                                    select new
                                    {
                                        CategoryId = g.Key,
                                        AveragePrice = g.Average(p => p.Price)
                                    };

        // Знаходження категорії з найбільшою середньою вартістю
        var highestAveragePriceCategory = categoryAveragePrices.OrderByDescending(c => c.AveragePrice).FirstOrDefault();

        // Отримання назви категорії
        var categoryName = categories.FirstOrDefault(c => c.Id == highestAveragePriceCategory?.CategoryId)?.Name;

        // Виведення результату
        if (categoryName != null)
        {
            Console.WriteLine($"Категорія з найбільшою середньою вартістю товару: {categoryName}, Середня вартість: {highestAveragePriceCategory.AveragePrice}");
        }
        else
        {
            Console.WriteLine("Немає даних про категорії");
        }
    }


    static void CustomersWithNoOrdersOrUnpaidOrders()
    {
        Console.WriteLine("Знаходження користувачів без замовлень або з неоплаченими замовленнями:");

        // Знайти користувачів без замовлень
        var customersWithNoOrders = users.Where(u => !orders.Any(o => o.UserId == u.Id));

        // Знайти користувачів з неоплаченими замовленнями
        var unpaidOrdersUsers = orders.Where(o => o.Status != "Paid").Select(o => o.UserId);
        var customersWithUnpaidOrders = users.Where(u => unpaidOrdersUsers.Contains(u.Id));

        // Вивести результат
        Console.WriteLine("Користувачі без замовлень:");
        foreach (var customer in customersWithNoOrders)
        {
            Console.WriteLine($"Користувач: {customer.FirstName} {customer.LastName}, Email: {customer.Email} (не робив замовлень)");
        }

        Console.WriteLine();

        Console.WriteLine("Користувачі з неоплаченими замовленнями:");
        foreach (var customer in customersWithUnpaidOrders)
        {
            Console.WriteLine($"Користувач: {customer.FirstName} {customer.LastName}, Email: {customer.Email} (має неоплачені замовлення)");
        }
    }

    static void CustomersWithTotalOrderAmountAboveAverage()
    {
        Console.WriteLine("Знаходження користувачів з загальною сумою замовлень вище середньої:");

        // Обчислення середньої суми усіх замовлень
        decimal averageOrderAmount = orders.Average(o => o.TotalPrice);

        // Знайти користувачів з загальною сумою замовлень вище середньої
        var customersAboveAverage = from order in orders
                                    group order by order.UserId into g
                                    let totalOrderAmount = g.Sum(o => o.TotalPrice)
                                    where totalOrderAmount > averageOrderAmount
                                    select new
                                    {
                                        UserId = g.Key,
                                        TotalOrderAmount = totalOrderAmount
                                    };
        // Вивести середню суму замовлень
        Console.WriteLine($"Середня сума замовлень: {averageOrderAmount}");
        // Вивести результат
        Console.WriteLine("Користувачі з загальною сумою замовлень вище середньої:");
        foreach (var customer in customersAboveAverage)
        {
            var userInfo = users.FirstOrDefault(u => u.Id == customer.UserId);
            if (userInfo != null)
            {
                Console.WriteLine($"Користувач: {userInfo.FirstName} {userInfo.LastName}, Email: {userInfo.Email}, " +
                                  $"Загальна сума замовлень: {customer.TotalOrderAmount}");
            }
        }
    }
    static void PopulateTestData()
    {
        // Заповнення даних для users, products, orders і orderDetails
    }
}























/*
using System;
using System.Collections.Generic;
using System.Linq;

public class User
{
    public int Id { get; set; }
    public string FirstName { get; set; }
    public string LastName { get; set; }
    public string Email { get; set; }
    public string Phone { get; set; }
}

public class Product
{
    public int Id { get; set; }
    public int CategoryId { get; set; }
    public string Model { get; set; }
    public int Year { get; set; }
    public double Price { get; set; }
    public string Color { get; set; }
}

public class Category
{
    public int Id { get; set; }
    public string Name { get; set; }
}

public class Order
{
    public int Id { get; set; }
    public DateTime CreatedDate { get; set; }
    public double TotalPrice { get; set; }
    public string Status { get; set; }
    public int UserId { get; set; }
    public string Address { get; set; }
}

public class OrderDetail
{
    public int Id { get; set; }
    public int OrderId { get; set; }
    public int ProductId { get; set; }
    public int Quantity { get; set; }
    public double Price { get; set; }
}

public class Program
{
    private static List<User> users = new List<User>();
    private static List<Product> products = new List<Product>();
    private static List<Category> categories = new List<Category>();
    private static List<Order> orders = new List<Order>();
    private static List<OrderDetail> orderDetails = new List<OrderDetail>();

    static void Main(string[] args)
    {
        // Add categories
        categories.Add(new Category { Id = 1, Name = "Smartphones" });
        categories.Add(new Category { Id = 2, Name = "Laptops" });
        categories.Add(new Category { Id = 3, Name = "Tablets" });
        categories.Add(new Category { Id = 4, Name = "Watches" });
        categories.Add(new Category { Id = 5, Name = "Fitness Trackers" });

        // Add users
        users.Add(new User { Id = 1, FirstName = "John", LastName = "Doe", Email = "john@example.com", Phone = "123456789" });
        users.Add(new User { Id = 2, FirstName = "Jane", LastName = "Smith", Email = "jane@example.com", Phone = "987654321" });
        users.Add(new User { Id = 3, FirstName = "Alice", LastName = "Johnson", Email = "alice@example.com", Phone = "555555555" });
        users.Add(new User { Id = 4, FirstName = "Bob", LastName = "Brown", Email = "bob@example.com", Phone = "444444444" });
        users.Add(new User { Id = 5, FirstName = "Charlie", LastName = "Wilson", Email = "charlie@example.com", Phone = "777777777" });

        // Add products
        products.Add(new Product { Id = 1, CategoryId = 1, Model = "iPhone 12", Year = 2020, Price = 999.99, Color = "Black" });
        products.Add(new Product { Id = 2, CategoryId = 2, Model = "MacBook Pro", Year = 2021, Price = 1499.99, Color = "Silver" });
        products.Add(new Product { Id = 3, CategoryId = 3, Model = "iPad Air", Year = 2020, Price = 599.99, Color = "Space Gray" });
        products.Add(new Product { Id = 4, CategoryId = 4, Model = "Samsung Galaxy S20", Year = 2021, Price = 899.99, Color = "White" });
        products.Add(new Product { Id = 5, CategoryId = 5, Model = "Fitbit Versa 3", Year = 2021, Price = 229.99, Color = "Black" });
        products.Add(new Product { Id = 6, CategoryId = 4, Model = "Garmin Forerunner 945", Year = 2019, Price = 599.99, Color = "Red" });
        products.Add(new Product { Id = 7, CategoryId = 5, Model = "Xiaomi Mi Band 6", Year = 2021, Price = 49.99, Color = "Blue" });
        products.Add(new Product { Id = 8, CategoryId = 4, Model = "Amazfit Bip U Pro", Year = 2020, Price = 69.99, Color = "Green" });
        products.Add(new Product { Id = 9, CategoryId = 2, Model = "Dell XPS 13", Year = 2021, Price = 1299.99, Color = "White" });
        products.Add(new Product { Id = 10, CategoryId = 2, Model = "Lenovo ThinkPad X1 Carbon", Year = 2021, Price = 1599.99, Color = "Gray" });
        products.Add(new Product { Id = 11, CategoryId = 2, Model = "Acer Aspire 5", Year = 2020, Price = 599.99, Color = "Silver" });
        products.Add(new Product { Id = 12, CategoryId = 2, Model = "ASUS ROG Strix G15", Year = 2021, Price = 1699.99, Color = "Black" });
        products.Add(new Product { Id = 13, CategoryId = 2, Model = "Microsoft Surface Laptop 4", Year = 2021, Price = 1499.99, Color = "Blue" });
        products.Add(new Product { Id = 14, CategoryId = 1, Model = "Samsung Galaxy S21", Year = 2021, Price = 1199.99, Color = "Phantom Gray" });
        products.Add(new Product { Id = 15, CategoryId = 1, Model = "Google Pixel 5", Year = 2020, Price = 699.99, Color = "Just Black" });
        products.Add(new Product { Id = 16, CategoryId = 1, Model = "OnePlus 9 Pro", Year = 2021, Price = 1069.99, Color = "Morning Mist" });


        new Order { Id = 1, CreatedDate = DateTime.Now, TotalPrice = 1000, Status = "New", UserId = 1, Address = "123 Main St" };
        new Order { Id = 2, CreatedDate = DateTime.Now.AddDays(-1), TotalPrice = 2000, Status = "Paid", UserId = 2, Address = "456 Oak St" };
        new Order { Id = 3, CreatedDate = DateTime.Now.AddDays(-1), TotalPrice = 1500, Status = "Paid", UserId = 2, Address = "456 Oak St" };
        new Order { Id = 4, CreatedDate = DateTime.Now.AddDays(-1), TotalPrice = 3000, Status = "Paid", UserId = 2, Address = "456 Oak St" };
        new Order { Id = 5, CreatedDate = DateTime.Now.AddDays(-2), TotalPrice = 2500, Status = "Delivered", UserId = 1, Address = "789 Elm St" };


        new OrderDetail { Id = 1, OrderId = 1, ProductId = 1, Quantity = 1, Price = 1000 };
        new OrderDetail { Id = 2, OrderId = 2, ProductId = 2, Quantity = 2, Price = 1800 };
        new OrderDetail { Id = 3, OrderId = 3, ProductId = 3, Quantity = 1, Price = 1500 };
      

        // Add sample data
        //AddSampleProduct();
        //AddSampleOrder();
        //AddSampleUnpaidOrder();

        // Call console menu
        ShowMenu();
    }

    static void ShowMenu()
    {
        Console.WriteLine("Console Menu");
        Console.WriteLine("a) Add Product");
        Console.WriteLine("b) Add Order");
        Console.WriteLine("c) Update Order Status");
        Console.WriteLine("d) Print Products by Category");
        Console.WriteLine("e) Find Regular Customers");
        Console.WriteLine("f) Find Store Revenue for a Period");
        Console.WriteLine("g) Find Top 5 Best Selling Products");
        Console.WriteLine("h) Find Most Popular Purchase Days");
        Console.WriteLine("i) Find Category with Highest Average Product Price");
        Console.WriteLine("j) Find Users with No Orders or Unpaid Orders");
        Console.WriteLine("k) Find Users with Total Orders Value Greater Than Average Order Value");
        Console.WriteLine("x) Exit");

        char choice = Console.ReadLine().ToLower()[0];
        switch (choice)
        {
            case 'a':
                AddProduct();
                break;
            case 'b':
                AddOrder();
                break;
            case 'c':
                UpdateOrderStatus();
                break;
            case 'd':
                PrintProductsByCategory();
                break;
            case 'e':
                FindRegularCustomers();
                break;
            case 'f':
                FindStoreRevenue();
                break;
            case 'g':
                FindTopSellingProducts();
                break;
            case 'h':
                FindPopularPurchaseDays();
                break;
            case 'i':
                FindCategoryWithHighestAveragePrice();
                break;
            case 'j':
                FindUsersWithNoOrUnpaidOrders();
                break;
            case 'k':
                FindUsersWithValueGreaterThanAverage();
                break;
            case 'x':
                Console.WriteLine("Exiting...");
                return;
            default:
                Console.WriteLine("Invalid choice.");
                break;
        }

        ShowMenu(); // Recursive call to continue with menu
    }

    static void AddProduct()
    {
        Console.WriteLine("Enter product details:");
        Console.Write("Model: ");
        string model = Console.ReadLine();
        Console.Write("Year: ");
        int year = int.Parse(Console.ReadLine());
        Console.Write("Price: ");
        double price = double.Parse(Console.ReadLine());
        Console.Write("Color: ");
        string color = Console.ReadLine();
        Console.Write("Category Id: ");
        int categoryId = int.Parse(Console.ReadLine());

        int newProductId = products.Count + 1; // Generate a new product id
        products.Add(new Product { Id = newProductId, CategoryId = categoryId, Model = model, Year = year, Price = price, Color = color });

        Console.WriteLine("Product added successfully.");
    }

    static void AddOrder()
    {
        Console.WriteLine("Enter order details:");
        Console.Write("User Id: ");
        int userId = int.Parse(Console.ReadLine());
        Console.Write("Address: ");
        string address = Console.ReadLine();
        Console.Write("Status: ");
        string status = Console.ReadLine();

        double totalPrice = 0;
        DateTime createdDate = DateTime.Now;

        int newOrderId = orders.Count + 1; // Generate a new order id
        orders.Add(new Order { Id = newOrderId, UserId = userId, Address = address, Status = status, CreatedDate = createdDate, TotalPrice = totalPrice });

        while (true)
        {
            Console.WriteLine("Enter order item details (enter 0 to finish):");
            Console.Write("Product Id: ");
            int productId = int.Parse(Console.ReadLine());
            if (productId == 0) break;
            Console.Write("Quantity: ");
            int quantity = int.Parse(Console.ReadLine());

            Product product = products.First(p => p.Id == productId);
            totalPrice += product.Price * quantity;

            int newOrderDetailId = orderDetails.Count + 1; // Generate a new order detail id
            orderDetails.Add(new OrderDetail { Id = newOrderDetailId, OrderId = newOrderId, ProductId = productId, Quantity = quantity, Price = product.Price });
        }

        Order order = orders.First(o => o.Id == newOrderId);
        order.TotalPrice = totalPrice;

        Console.WriteLine("Order added successfully.");
    }

    static void UpdateOrderStatus()
    {
        Console.WriteLine("Enter order ID to update:");
        int orderId = int.Parse(Console.ReadLine());
        Console.WriteLine("Enter new status:");
        string newStatus = Console.ReadLine();

        Order order = orders.FirstOrDefault(o => o.Id == orderId);
        if (order != null)
        {
            order.Status = newStatus;
            Console.WriteLine("Order status updated successfully.");
        }
        else
        {
            Console.WriteLine("Order not found.");
        }
    }

    static void PrintProductsByCategory()
    {
        Console.WriteLine("Enter category ID:");
        int categoryId = int.Parse(Console.ReadLine());

        var productsByCategory = products.Where(p => p.CategoryId == categoryId).ToList();
        if (productsByCategory.Any())
        {
            Console.WriteLine($"Products in category {categoryId}:");
            foreach (var product in productsByCategory)
            {
                Console.WriteLine($"ID: {product.Id}, Model: {product.Model}, Year: {product.Year}, Price: {product.Price}, Color: {product.Color}");
            }
        }
        else
        {
            Console.WriteLine("No products found in this category.");
        }
    }

    static void FindRegularCustomers()
    {
        // A regular customer is defined as someone who has placed at least 5 orders
        var regularCustomers = users.Where(u => orders.Count(o => o.UserId == u.Id) >= 5).ToList();

        if (regularCustomers.Any())
        {
            Console.WriteLine("Regular Customers:");
            foreach (var customer in regularCustomers)
            {
                Console.WriteLine($"ID: {customer.Id}, Name: {customer.FirstName} {customer.LastName}, Email: {customer.Email}");
            }
        }
        else
        {
            Console.WriteLine("No regular customers found.");
        }
    }

    static void FindStoreRevenue()
    {
        Console.WriteLine("Enter start date (yyyy-mm-dd):");
        DateTime startDate = DateTime.Parse(Console.ReadLine());
        Console.WriteLine("Enter end date (yyyy-mm-dd):");
        DateTime endDate = DateTime.Parse(Console.ReadLine());

        var totalRevenue = orders
            .Where(o => o.CreatedDate >= startDate && o.CreatedDate <= endDate && o.Status == "Paid")
            .Sum(o => o.TotalPrice);

        Console.WriteLine($"Total revenue from {startDate.ToShortDateString()} to {endDate.ToShortDateString()} is {totalRevenue:C}");
    }

    static void FindTopSellingProducts()
    {
        var topSellingProducts = orderDetails
            .GroupBy(od => od.ProductId)
            .Select(g => new { ProductId = g.Key, QuantitySold = g.Sum(od => od.Quantity) })
            .OrderByDescending(g => g.QuantitySold)
            .Take(5)
            .Join(products, g => g.ProductId, p => p.Id, (g, p) => new { p.Model, g.QuantitySold })
            .ToList();

        Console.WriteLine("Top 5 best selling products:");
        foreach (var product in topSellingProducts)
        {
            Console.WriteLine($"Model: {product.Model}, Quantity Sold: {product.QuantitySold}");
        }
    }

    static void FindPopularPurchaseDays()
    {
        var popularDays = orders
            .GroupBy(o => o.CreatedDate.DayOfWeek)
            .Select(g => new { DayOfWeek = g.Key, OrderCount = g.Count() })
            .OrderByDescending(g => g.OrderCount)
            .ToList();

        Console.WriteLine("Most popular purchase days:");
        foreach (var day in popularDays)
        {
            Console.WriteLine($"{day.DayOfWeek}: {day.OrderCount} orders");
        }
    }

    static void FindCategoryWithHighestAveragePrice()
    {
        var categoryWithHighestAvgPrice = products
            .GroupBy(p => p.CategoryId)
            .Select(g => new { CategoryId = g.Key, AvgPrice = g.Average(p => p.Price) })
            .OrderByDescending(g => g.AvgPrice)
            .FirstOrDefault();

        if (categoryWithHighestAvgPrice != null)
        {
            var categoryName = categories.FirstOrDefault(c => c.Id == categoryWithHighestAvgPrice.CategoryId)?.Name;
            Console.WriteLine($"Category with highest average product price: {categoryName} ({categoryWithHighestAvgPrice.AvgPrice:C})");
        }
        else
        {
            Console.WriteLine("No categories found.");
        }
    }

    static void FindUsersWithNoOrUnpaidOrders()
    {
        var usersWithNoOrUnpaidOrders = users
            .Where(u => !orders.Any(o => o.UserId == u.Id && o.Status == "Paid"))
            .Select(u => new { u.Id, u.FirstName, u.LastName })
            .ToList();

        if (usersWithNoOrUnpaidOrders.Any())
        {
            Console.WriteLine("Users with no orders or only unpaid orders:");
            foreach (var user in usersWithNoOrUnpaidOrders)
            {
                Console.WriteLine($"ID: {user.Id}, Name: {user.FirstName} {user.LastName}");
            }
        }
        else
        {
            Console.WriteLine("All users have paid orders.");
        }
    }

    static void FindUsersWithValueGreaterThanAverage()
    {
        var averageOrderValue = orders.Where(o => o.Status == "Paid").Average(o => o.TotalPrice);

        var usersWithValueGreaterThanAverage = users
            .Where(u => orders.Where(o => o.UserId == u.Id && o.Status == "Paid").Sum(o => o.TotalPrice) > averageOrderValue)
            .Select(u => new { u.Id, u.FirstName, u.LastName })
            .ToList();

        Console.WriteLine("Users with total orders value greater than average order value:");
        foreach (var user in usersWithValueGreaterThanAverage)
        {
            Console.WriteLine($"ID: {user.Id}, Name: {user.FirstName} {user.LastName}");
        }
    }

    static void AddSampleProduct()
    {
        Console.WriteLine("Adding sample product...");
        products.Add(new Product { Id = products.Count + 1, CategoryId = 1, Model = "Sample Phone", Year = 2021, Price = 199.99, Color = "Black" });
        Console.WriteLine("Sample product added successfully.");
    }

    static void AddSampleOrder()
    {
        Console.WriteLine("Adding sample order...");
        int newOrderId = orders.Count + 1;
        orders.Add(new Order
        {
            Id = newOrderId,
            CreatedDate = DateTime.Now,
            TotalPrice = 0,
            Status = "Pending",
            UserId = 1,
            Address = "Sample Address"
        });

        int newOrderDetailId = orderDetails.Count + 1;
        orderDetails.Add(new OrderDetail
        {
            Id = newOrderDetailId,
            OrderId = newOrderId,
            ProductId = 1,
            Quantity = 1,
            Price = 199.99
        });

        Order order = orders.First(o => o.Id == newOrderId);
        order.TotalPrice = 199.99;
        Console.WriteLine("Sample order added successfully.");
    }

    static void AddSampleUnpaidOrder()
    {
        Console.WriteLine("Adding sample unpaid order...");
        int newOrderId = orders.Count + 1;
        orders.Add(new Order
        {
            Id = newOrderId,
            CreatedDate = DateTime.Now,
            TotalPrice = 0,
            Status = "Unpaid",
            UserId = 2,
            Address = "Sample Unpaid Address"
        });

        int newOrderDetailId = orderDetails.Count + 1;
        orderDetails.Add(new OrderDetail
        {
            Id = newOrderDetailId,
            OrderId = newOrderId,
            ProductId = 2,
            Quantity = 1,
            Price = 1499.99
        });

        Order order = orders.First(o => o.Id == newOrderId);
        order.TotalPrice = 1499.99;
        Console.WriteLine("Sample unpaid order added successfully.");
    }
}



*/