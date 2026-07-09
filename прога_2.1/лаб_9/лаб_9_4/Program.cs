using System;
using System.Reflection;
using System.Text;

// Атрибут для вказівки на назву таблиці
[AttributeUsage(AttributeTargets.Class)]
public class TableAttribute : Attribute
{
    public string TableName { get; }

    public TableAttribute(string tableName)
    {
        TableName = tableName;
    }
}

// Атрибут для вказівки на назву колонки
[AttributeUsage(AttributeTargets.Property)]
public class ColumnAttribute : Attribute
{
    public string ColumnName { get; }

    public ColumnAttribute(string columnName)
    {
        ColumnName = columnName;
    }
}

// Приклад класу з атрибутами Table і Column
[Table("Products")]
public class Product
{
    [Column("Id")]
    public int Id { get; set; }

    [Column("FullName")]
    public string Name { get; set; }

   
    public decimal Price { get; set; }

    // Метод для генерації INSERT запиту
    public string GenerateInsertQuery()
    {
        StringBuilder query = new StringBuilder();
        Type type = GetType();

        // Отримуємо назву таблиці
        TableAttribute tableAttribute = (TableAttribute)type.GetCustomAttribute(typeof(TableAttribute));
        string tableName = tableAttribute != null ? tableAttribute.TableName : type.Name;

        query.AppendFormat("INSERT INTO {0} (", tableName);

        // Отримуємо назви колонок і значення властивостей
        PropertyInfo[] properties = type.GetProperties();
        foreach (PropertyInfo property in properties)
        {
            ColumnAttribute columnAttribute = (ColumnAttribute)property.GetCustomAttribute(typeof(ColumnAttribute));
            string columnName = columnAttribute != null ? columnAttribute.ColumnName : property.Name;

            query.AppendFormat("{0}, ", columnName);
        }
        query.Remove(query.Length - 2, 2); // Видаляємо останню кому

        query.Append(") VALUES (");

        foreach (PropertyInfo property in properties)
        {
            object value = property.GetValue(this);
            query.AppendFormat("'{0}', ", value);
        }
        query.Remove(query.Length - 2, 2); // Видаляємо останню кому

        query.Append(");");

        return query.ToString();
    }
}

class Program
{
    static void Main(string[] args)
    {
        // Створюємо екземпляр класу Product
        Product product = new Product
        {
            Id = 1,
            Name = "Laptop",
            Price = 999.99m
        };

        // Генеруємо INSERT запит для екземпляра класу Product
        string insertQuery = product.GenerateInsertQuery();
        Console.WriteLine(insertQuery);
    }
}
