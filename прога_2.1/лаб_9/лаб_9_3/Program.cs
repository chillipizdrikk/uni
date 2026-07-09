using System;
using System.Linq;
using System.Reflection;

[AttributeUsage(AttributeTargets.Class)]
public class SingletonServiceAttribute : Attribute
{
    public Type ServiceType { get; }

    public SingletonServiceAttribute(Type serviceType)
    {
        ServiceType = serviceType;
    }
}
public class ServiceResolver
{
    public T GetService<T>()
    {
        var interfaceType = typeof(T);
        var assembly = interfaceType.Assembly; // Збірка інтерфейсу

        var implementationType = assembly.GetTypes()
            .Where(t => interfaceType.IsAssignableFrom(t) && t.GetCustomAttribute<SingletonServiceAttribute>() != null && t.GetInterfaces().Contains(interfaceType))
            .FirstOrDefault();

        if (implementationType == null)
        {
            throw new Exception($"No implementation of {interfaceType.Name} marked with SingletonServiceAttribute found in the same assembly.");
        }

        return (T)Activator.CreateInstance(implementationType);
    }
}


// Test interfaces and implementations
public interface ITestService
{
    void TestMethod();
}

[SingletonService(typeof(ITestService))]
public class TestService : ITestService
{
    public void TestMethod()
    {
        Console.WriteLine("Test method executed from TestService.");
    }
}


public class Program
{
    public static void Main()
    {
        var resolver = new ServiceResolver();
        var service = resolver.GetService<ITestService>();
        Console.WriteLine($"Type of the obtained service: {service.GetType().Name}");
        service.TestMethod();
    }
}

