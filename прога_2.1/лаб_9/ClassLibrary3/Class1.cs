namespace ClassLibrary3
{
    public interface IPlugin
    {
        double Execute(double a, double b);
    }

    public class Addition : IPlugin
    {
        public double Execute(double a, double b)
        {
            return a + b;
        }
    }

    public class Subtraction : IPlugin
    {
        public double Execute(double a, double b)
        {
            return a - b;
        }
    }

    public class Multiplication : IPlugin
    {
        public double Execute(double a, double b)
        {
            return a * b;
        }
    }
    class Program
    {
        static void Main(string[] args)
        {
            // Використовуємо повне ім'я типу з простором імен
            ClassLibrary3.IPlugin multiplication = new Multiplication();

            double a = 5;
            double b = 3;

            Console.WriteLine($"Multiplication: {multiplication.Execute(a, b)}");
        }
    }
}
