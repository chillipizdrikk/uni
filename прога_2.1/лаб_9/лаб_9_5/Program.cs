using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;

namespace PluginLoader
{
    // Атрибут, що позначає клас як тестовий клас
    [AttributeUsage(AttributeTargets.Class, Inherited = false, AllowMultiple = false)]
    public sealed class TestClassAttribute : Attribute
    {
    }

    // Атрибут, що позначає метод як тестовий метод
    [AttributeUsage(AttributeTargets.Method, Inherited = false, AllowMultiple = false)]
    public sealed class TestMethodAttribute : Attribute
    {
    }

    // Атрибут, що позначає тестовий метод і визначає його параметри
    [AttributeUsage(AttributeTargets.Method, Inherited = false, AllowMultiple = true)]
    public sealed class TestCaseAttribute : Attribute
    {
        public object[] Parameters { get; }

        public TestCaseAttribute(params object[] parameters)
        {
            Parameters = parameters;
        }
    }

    // Клас, який відповідає за запуск тестів
    public class TestRunner
    {
        public static void RunTests()
        {
            Assembly[] assemblies = AppDomain.CurrentDomain.GetAssemblies();

            // Проходимося по всіх зборках
            foreach (Assembly assembly in assemblies)
            {
                // Проходимося по всіх типах (класах) в збірці
                foreach (Type type in assembly.GetTypes())
                {
                    // Перевіряємо, чи клас має атрибут TestClassAttribute
                    if (type.IsDefined(typeof(TestClassAttribute), false))
                    {
                        // Виводимо повідомлення про початок тестування класу
                        Console.WriteLine($"Running tests in class: {type.Name}");

                        // Створюємо екземпляр класу
                        object instance = Activator.CreateInstance(type);

                        // Проходимося по всіх методах класу
                        foreach (MethodInfo method in type.GetMethods())
                        {
                            // Перевіряємо, чи метод має атрибут TestMethodAttribute
                            if (method.IsDefined(typeof(TestMethodAttribute), false))
                            {
                                // Виводимо повідомлення про початок тестування методу
                                Console.WriteLine($"Running test: {type.Name}.{method.Name}");

                                // Отримуємо атрибути TestCaseAttribute для методу
                                var testCaseAttributes = method.GetCustomAttributes<TestCaseAttribute>().ToList();

                                // Якщо немає атрибутів TestCaseAttribute, запускаємо метод без параметрів
                                if (testCaseAttributes.Count == 0)
                                {
                                    try
                                    {
                                        method.Invoke(instance, null);
                                        Console.WriteLine($"Test {method.Name} passed.");
                                    }
                                    catch (Exception ex)
                                    {
                                        Console.WriteLine($"Test {method.Name} failed: {ex.Message}");
                                    }
                                }
                                // Якщо є атрибути TestCaseAttribute, запускаємо метод з параметрами
                                else
                                {
                                    foreach (var testCaseAttribute in testCaseAttributes)
                                    {
                                        try
                                        {
                                            method.Invoke(instance, testCaseAttribute.Parameters);
                                            Console.WriteLine($"Test {method.Name} passed.");
                                        }
                                        catch (Exception ex)
                                        {
                                            Console.WriteLine($"Test {method.Name} failed: {ex.Message}");
                                        }
                                    }
                                }
                            }
                        }
                        // Додаємо порожній рядок після всіх тестів класу
                        Console.WriteLine();
                    }
                }
            }
        }
    }

    // Клас з математичними функціями
    public class MathFunctions
    {
        public int Add(int a, int b)
        {
            return a + b;
        }

        public int Divide(int a, int b)
        {
            return a / b;
        }

        public int Power(int a, int b)
        {
            return (int)Math.Pow(a, b);
        }
    }

    // Тестовий клас
    [TestClass]
    public class CalculatorTests
    {
        MathFunctions math = new MathFunctions();

        // Тест для функції Add
        [TestMethod]
        [TestCase(1, 1, 2)]
        [TestCase(2, 3, 5)]
        public void Add(int a, int b, int expectedResult)
        {
            int result = math.Add(a, b);
            if (result != expectedResult)
            {
                throw new Exception($"Add test failed. Expected: {expectedResult}, Actual: {result}");
            }
        }

        // Тест для функції Divide
        [TestMethod]
        [TestCase(6, 2, 3)]
        [TestCase(9, 3, 3)]
        public void Divide(int a, int b, int expectedResult)
        {
            int result = math.Divide(a, b);
            if (result != expectedResult)
            {
                throw new Exception($"Divide test failed. Expected: {expectedResult}, Actual: {result}");
            }
        }

        // Тест для функції Power
        [TestMethod]
        [TestCase(2, 3, 8)]
        [TestCase(4, 2, 16)]
        public void Power(int a, int b, int expectedResult)
        {
            int result = math.Power(a, b);
            if (result != expectedResult)
            {
                throw new Exception($"Power test failed. Expected: {expectedResult}, Actual: {result}");
            }
        }
    }

    // Основний клас програми
    public class Program
    {
        public static void Main()
        {
            TestRunner.RunTests();
        }
    }
}
