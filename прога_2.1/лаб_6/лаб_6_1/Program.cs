using System;
using System.Text;

// Інтерфейс з методом для отримання знижки
public interface IGetDiscount<in T>
{
    decimal GetDiscount(T item);
}

// Батьківський клас продукту
public class Product
{
    public string Name { get; set; }
    public decimal Price { get; set; }

    public Product(string name, decimal price)
    {
        Name = name;
        Price = price;
    }
}

// Клас, що реалізує інтерфейс для знижки на звичайний продукт
public class DiscountCalculator : IGetDiscount<Product>
{
    public decimal GetDiscount(Product item)
    {
        // Приклад обчислення знижки для продукту
        decimal discount = 0.1m; // Наприклад, 10% знижка
        return discount;
    }
}

// Похідний клас від Товар
public class SpecialProduct : Product
{
    public SpecialProduct(string name, decimal price) : base(name, price) { }
}

// Клас, що реалізує інтерфейс для знижки на спеціальний продукт
public class SpecialDiscountCalculator : IGetDiscount<SpecialProduct>
{
    public decimal GetDiscount(SpecialProduct item)
    {
        // Обчислення спеціальної знижки для спеціального продукту
        decimal discount = 0.2m; // Наприклад, 20% знижка
        return discount;
    }
}

class Program
{
    static void Main(string[] args)
    {
        Console.OutputEncoding = Encoding.UTF8; // Встановлення кодування виведення консолі UTF-8

        var product = new Product("Товар", 100);
        var discountCalculator = new DiscountCalculator();
        decimal discountPercentage = discountCalculator.GetDiscount(product) * 100; // Переведення відношення відсотка
        Console.WriteLine($"Знижка на звичайний продукт: {discountPercentage}%");

        var specialProduct = new SpecialProduct("Спеціальний товар", 100);
        var specialDiscountCalculator = new SpecialDiscountCalculator();
        discountPercentage = specialDiscountCalculator.GetDiscount(specialProduct) * 100; // Переведення відношення відсотка
        Console.WriteLine($"Знижка на спеціальний продукт: {discountPercentage}%");
    }
}
