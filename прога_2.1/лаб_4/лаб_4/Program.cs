using System;
using System.Collections.Generic;
using System.Linq;

public abstract class Furniture : IComparable<Furniture>
{
    public string Model { get; set; }
    public double Price { get; set; }

    public Furniture(string model, double price)
    {
        Model = model;
        Price = price;
    }

    public abstract double GetDiscountedPrice();

    public int CompareTo(Furniture other)
    {
        return other.Price.CompareTo(this.Price);
    }
}

public class Chair : Furniture
{
    public Chair(string model, double price) : base(model, price) { }

    public override double GetDiscountedPrice()
    {
        return Price * 0.9;
    }
}

public class Bed : Furniture
{
    public Bed(string model, double price) : base(model, price) { }

    public override double GetDiscountedPrice()
    {
        return Price * 0.95;
    }
}

public class Table : Furniture
{
    public Table(string model, double price) : base(model, price) { }

    public override double GetDiscountedPrice()
    {
        return Price * 0.8;
    }
}

public class ModelComparer : IComparer<Furniture>
{
    public int Compare(Furniture x, Furniture y)
    {
        return string.Compare(x.Model, y.Model);
    }
}

class Program
{
    static void Main(string[] args)
    {
        List<Furniture> purchasedFurniture = new List<Furniture>();

        while (true)
        {
            Console.WriteLine("Введiть тип меблiв (Chair(C), Bed(B), Table(T)) або 'exit' для виходу:");
            string type = Console.ReadLine();

            if (type.ToLower() == "exit") break;

            Console.WriteLine("Введiть модель:");
            string model = Console.ReadLine();

            Console.WriteLine("Введiть цiну:");
            double price = Convert.ToDouble(Console.ReadLine());

            switch (type)
            {
                case "C":
                    purchasedFurniture.Add(new Chair(model, price));
                    break;
                case "B":
                    purchasedFurniture.Add(new Bed(model, price));
                    break;
                case "T":
                    purchasedFurniture.Add(new Table(model, price));
                    break;
            }
        }

        //сортування в порядку зростання
        purchasedFurniture.Sort((x, y) => y.GetDiscountedPrice().CompareTo(x.GetDiscountedPrice()));
        Console.WriteLine("Список меблiв, вiдсортований за цiною зi знижкою в порядку спадання:");
        foreach (var furniture in purchasedFurniture)
        {
            Console.WriteLine($"Категорiя: {furniture}, Модель: {furniture.Model}, Цiна зi знижкою: {furniture.GetDiscountedPrice()}");
        }

        //сортування за моделлю
        purchasedFurniture.Sort(new ModelComparer());
        Console.WriteLine("\nСписок меблiв, вiдсортований за назвою моделi:");
        foreach (var furniture in purchasedFurniture)
        {
            Console.WriteLine($"Категорiя: {furniture}, Модель: {furniture.Model}, Цiна зi знижкою: {furniture.GetDiscountedPrice()}");
        }

        //друкуємо загальну суму придбаних меблів
        double totalPrice = purchasedFurniture.Sum(furniture => furniture.GetDiscountedPrice());
        Console.WriteLine($"\nЗагальна сума придбаних меблiв зi знижкою: {totalPrice}");

        //друкуємо загальну суму за категорією
        var categoryTotals = purchasedFurniture.GroupBy(furniture => furniture.GetType().Name)
            .Select(group => new { Category = group.Key, TotalPrice = group.Sum(furniture => furniture.GetDiscountedPrice()) });

        Console.WriteLine("\nСума придбаних меблiв зi знижкою для кожної категорiї:");
        foreach (var categoryTotal in categoryTotals)
        {
            Console.WriteLine($"Категорiя {categoryTotal.Category}: {categoryTotal.TotalPrice}");
        }
    }
}
