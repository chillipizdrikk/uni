using System;
using System.Collections.Generic;
using System.Linq;

public class User
{
    public int Id { get; set; }
    public string FirstName { get; set; }
    public string LastName { get; set; }
    public string Email { get; set; }
    public string PhoneNumber { get; set; }
}

public enum OrderType
{
    FirstName,
    LastName,
    Email,
    PhoneNumber
}

public class SearchUserRequest
{
    public string SearchText { get; set; }
    public int PageNumber { get; set; }
    public int ItemsPerPage { get; set; }
    public OrderType OrderType { get; set; }
    public bool Asc { get; set; }
}

public class UserService
{
    private List<User> users = new List<User>
    {
        new User { Id = 1, FirstName = "John", LastName = "Smith", Email = "john.smith@example.com", PhoneNumber = "+380501234567" },
        new User { Id = 2, FirstName = "Oliver", LastName = "Taylor", Email = "oliver.taylor@example.com", PhoneNumber = "+380501234568" },
        new User { Id = 3, FirstName = "Emma", LastName = "Johnson", Email = "emma.johnson@example.com", PhoneNumber = "+380501234569" },
        new User { Id = 4, FirstName = "James", LastName = "Brown", Email = "james.brown@example.com", PhoneNumber = "+380501234570" },
        new User { Id = 5, FirstName = "Sophia", LastName = "Williams", Email = "sophia.williams@example.com", PhoneNumber = "+380501234571" },
        new User { Id = 6, FirstName = "William", LastName = "Jones", Email = "william.jones@example.com", PhoneNumber = "+380501234572" },
        new User { Id = 7, FirstName = "Olivia", LastName = "Miller", Email = "olivia.miller@example.com", PhoneNumber = "+380501234573" },
        new User { Id = 8, FirstName = "Alexander", LastName = "Davis", Email = "alexander.davis@example.com", PhoneNumber = "+380501234574" },
        new User { Id = 9, FirstName = "Ethan", LastName = "Wilson", Email = "ethan.wilson@example.com", PhoneNumber = "+380501234575" },
        new User { Id = 10, FirstName = "Mia", LastName = "Moore", Email = "mia.moore@example.com", PhoneNumber = "+380501234576" },
        new User { Id = 11, FirstName = "Natalie", LastName = "Clark", Email = "natalie.clark@example.com", PhoneNumber = "+380501234577" },
        new User { Id = 12, FirstName = "John", LastName = "Johnson", Email = "john.johnson@example.com", PhoneNumber = "+380501234578" }
    };

    public IList<User> SearchUsers(SearchUserRequest request)
    {
        IEnumerable<User> filteredUsers = users;

        if (!string.IsNullOrEmpty(request.SearchText))
        {
            filteredUsers = filteredUsers.Where(u =>
                u.FirstName.Contains(request.SearchText, StringComparison.OrdinalIgnoreCase) ||
                u.LastName.Contains(request.SearchText, StringComparison.OrdinalIgnoreCase) ||
                u.Email.Contains(request.SearchText, StringComparison.OrdinalIgnoreCase) ||
                u.PhoneNumber.Contains(request.SearchText, StringComparison.OrdinalIgnoreCase));
        }

        switch (request.OrderType)
        {
            case OrderType.FirstName:
                filteredUsers = request.Asc ? filteredUsers.OrderBy(u => u.FirstName) : filteredUsers.OrderByDescending(u => u.FirstName);
                break;
            case OrderType.LastName:
                filteredUsers = request.Asc ? filteredUsers.OrderBy(u => u.LastName) : filteredUsers.OrderByDescending(u => u.LastName);
                break;
            case OrderType.Email:
                filteredUsers = request.Asc ? filteredUsers.OrderBy(u => u.Email) : filteredUsers.OrderByDescending(u => u.Email);
                break;
            case OrderType.PhoneNumber:
                filteredUsers = request.Asc ? filteredUsers.OrderBy(u => u.PhoneNumber) : filteredUsers.OrderByDescending(u => u.PhoneNumber);
                break;
        }

        if (request.ItemsPerPage > 0)
        {
            int skip = (request.PageNumber - 1) * request.ItemsPerPage;
            filteredUsers = filteredUsers.Skip(skip).Take(request.ItemsPerPage);
        }

        return filteredUsers.ToList();
    }
}

class Program
{
    static void Main()
    {
        UserService userService = new UserService();

        while (true)
        {
            Console.WriteLine("Введіть параметри пошуку:");
            Console.Write("Текст пошуку: ");
            string searchText = Console.ReadLine();

            Console.Write("Номер сторінки: ");
            if (!int.TryParse(Console.ReadLine(), out int pageNumber))
            {
                Console.WriteLine("Невірний ввід для номера сторінки. Спробуйте ще раз.");
                continue;
            }

            Console.Write("Кількість елементів на сторінці (або 0, щоб показати всіх користувачів): ");
            if (!int.TryParse(Console.ReadLine(), out int itemsPerPage))
            {
                Console.WriteLine("Невірний ввід для кількості елементів на сторінці. Спробуйте ще раз.");
                continue;
            }

            Console.Write("Тип сортування (0 - за ім'ям, 1 - за прізвищем, 2 - за email, 3 - за номером телефону): ");
            if (!int.TryParse(Console.ReadLine(), out int orderTypeInput) || !Enum.IsDefined(typeof(OrderType), orderTypeInput))
            {
                Console.WriteLine("Невірний ввід для типу сортування. Спробуйте ще раз.");
                continue;
            }
            OrderType orderType = (OrderType)orderTypeInput;

            Console.Write("Сортувати за зростанням (true/false): ");
            if (!bool.TryParse(Console.ReadLine(), out bool asc))
            {
                Console.WriteLine("Невірний ввід для сортування. Спробуйте ще раз.");
                continue;
            }

            SearchUserRequest request = new SearchUserRequest
            {
                SearchText = searchText,
                PageNumber = pageNumber,
                ItemsPerPage = itemsPerPage,
                OrderType = orderType,
                Asc = asc
            };

            var users = userService.SearchUsers(request);

            Console.WriteLine($"Результати пошуку для \"{request.SearchText}\" на сторінці {request.PageNumber}:");
            foreach (var user in users)
            {
                Console.WriteLine($"ID: {user.Id}, Ім'я: {user.FirstName}, Прізвище: {user.LastName}, Email: {user.Email}, Телефон: {user.PhoneNumber}");
            }

            Console.Write("Продовжити пошук? (yes/no): ");
            string continueSearch = Console.ReadLine().ToLower();
            if (continueSearch != "yes")
                break;

            Console.WriteLine();
        }
    }
}
