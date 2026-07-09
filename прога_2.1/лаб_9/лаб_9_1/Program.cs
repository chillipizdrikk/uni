using System;
using System.Reflection;

// Створюємо атрибут AlternativeName
public class AlternativeNameAttribute : Attribute
{
    public string Name { get; private set; }

    public AlternativeNameAttribute(string name)
    {
        Name = name;
    }
}

// Створюємо enum і використовуємо атрибут AlternativeName
public enum MyEnum
{
    [AlternativeName("Перше")]
    First,

    [AlternativeName("Друге")]
    Second,

 
    Third
}

public static class EnumExtensions
{
    // Метод-розширення, що отримує альтернативну назву для значення з enum
    public static string GetAlternativeName(this Enum value)
    {
        FieldInfo field = value.GetType().GetField(value.ToString());

        AlternativeNameAttribute attribute
                = Attribute.GetCustomAttribute(field, typeof(AlternativeNameAttribute))
                    as AlternativeNameAttribute;

        return attribute == null ? value.ToString() : attribute.Name;
    }
}

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine(MyEnum.First.GetAlternativeName());  // Виведе "Перше"
        Console.WriteLine(MyEnum.Second.GetAlternativeName()); // Виведе "Друге"
        Console.WriteLine(MyEnum.Third.GetAlternativeName());  // Виведе "Третє"
    }
}
