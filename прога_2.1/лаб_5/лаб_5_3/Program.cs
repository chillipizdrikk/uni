using System;
using System.Collections.Generic;
using System.Linq.Expressions;
using System.Text;

public class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    public string Email { get; set; }
}
public class QueryBuilder
{
    public static string Select<T>(Expression<Func<T, object>> projection, Dictionary<Expression<Func<T, object>>, object> filter)
    {
        var tableName = typeof(T).Name;
        var selectField = GetMemberName(projection.Body);
        var whereClause = filter.Count > 0 ? " WHERE " + BuildWhereClause(filter) : "";

        return $"SELECT {selectField} FROM {tableName}{whereClause}";
    }

    private static string GetMemberName(Expression expression)
    {
        switch (expression)
        {
            case MemberExpression m:
                return m.Member.Name;
            case UnaryExpression u when u.Operand is MemberExpression m:
                return m.Member.Name;
            default:
                throw new NotImplementedException(expression.GetType().ToString());
        }
    }

    private static string BuildWhereClause<T>(Dictionary<Expression<Func<T, object>>, object> filter)
    {
        var builder = new StringBuilder();

        foreach (var item in filter)
        {
            if (builder.Length > 0)
            {
                builder.Append(" AND ");
            }

            var memberName = GetMemberName(item.Key.Body);
            builder.Append($"{memberName} = '{item.Value}'");
        }

        return builder.ToString();
    }

    public static void Main(string[] args)
    {
        var filter = new Dictionary<Expression<Func<Person, object>>, object>
        {
            { p => p.Age, 30 },
            { p => p.Email, "test@gmail.com" }
        };

        string result = QueryBuilder.Select<Person>(p => p.Name, filter);

        Console.WriteLine(result);

        var filter1 = new Dictionary<Expression<Func<Person, object>>, object>();

        string result1 = QueryBuilder.Select<Person>(p => p.Name, filter1);

        Console.WriteLine(result1);
    }
}
