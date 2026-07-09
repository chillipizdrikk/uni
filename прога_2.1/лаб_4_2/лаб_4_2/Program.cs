using System;


abstract class ConsoleWindow
{
    public abstract void Paint();
}

class WinConsoleWindow : ConsoleWindow
{
    public override void Paint()
    {
        Console.WriteLine("Painting for Windows...");
        Console.ForegroundColor = ConsoleColor.Yellow;
        Console.BackgroundColor = ConsoleColor.Blue;
        Console.WindowHeight = 20;
        Console.WindowWidth = 40;
       
    }
}

class MacConsoleWindow : ConsoleWindow
{
    public override void Paint()
    {
        Console.WriteLine("Painting for Mac...");
        Console.ForegroundColor = ConsoleColor.Cyan;
        Console.BackgroundColor = ConsoleColor.Magenta;
        Console.WindowHeight = 25;
        Console.WindowWidth = 50;
       
    }

    //визначаємо метод createConsoleWindow
    public void CreateConsoleWindow()
    {
        Console.WriteLine("Creating console window for Mac...");
    }
}

class LinuxConsoleWindow : ConsoleWindow
{
    public override void Paint()
    {
        Console.WriteLine("Painting for Linux...");
        Console.ForegroundColor = ConsoleColor.Green;
        Console.BackgroundColor = ConsoleColor.DarkRed;
        Console.WindowHeight = 30;
        Console.WindowWidth = 60;
    }

    //визначаємо метод createConsoleWindow
    public void CreateConsoleWindow()
    {
        Console.WriteLine("Creating console window for Linux...");
    }
}

// Інтерфейс фабрики вікон консолі
interface IConsoleFactory
{
    ConsoleWindow CreateConsoleWindow();
}

// Фабрики вікон консолі для різних операційних систем
class WinConsoleFactory : IConsoleFactory
{
    public ConsoleWindow CreateConsoleWindow()
    {
        return new WinConsoleWindow();
    }
}

class MacConsoleFactory : IConsoleFactory
{
    public ConsoleWindow CreateConsoleWindow()
    {
        return new MacConsoleWindow();
    }
}

class LinuxConsoleFactory : IConsoleFactory
{
    public ConsoleWindow CreateConsoleWindow()
    {
        return new LinuxConsoleWindow();
    }
}

// Клас додатку
class Application
{
    private readonly IConsoleFactory _factory;
    private readonly ConsoleWindow _consoleWindow;

    public Application(IConsoleFactory factory)
    {
        _factory = factory;
        _consoleWindow = _factory.CreateConsoleWindow();
    }

    public void CreateUI()
    {
        // Логіка створення користувацького інтерфейсу
        Console.WriteLine("Creating UI...");
    }

    public void Paint()
    {
        _consoleWindow.Paint();
    }
}

class Program
{
    static void Main(string[] args)
    {
        if (args.Length != 1)
        {
            Console.WriteLine("MyApp <OS>");
            return;
        }

        string os = args[0].ToLower();

        IConsoleFactory factory;
        switch (os)
        {
            case "windows":
                factory = new WinConsoleFactory();
                break;
            case "mac":
                factory = new MacConsoleFactory();
                break;
            case "linux":
                factory = new LinuxConsoleFactory();
                break;
            default:
                Console.WriteLine("Unsupported OS.");
                return;
        }

        var app = new Application(factory);

        if (factory is MacConsoleFactory macFactory)
        {
            macFactory.CreateConsoleWindow();
        }
        else if (factory is LinuxConsoleFactory linuxFactory)
        {
            linuxFactory.CreateConsoleWindow();
        }

        app.CreateUI();
        app.Paint();

        Console.WriteLine("Application executed successfully!");
    }
}
