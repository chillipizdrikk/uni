using System;
using System.IO;
using System.Reflection;
using ClassLibrary1;

class Program
{
    static void Main(string[] args)
    {
        // Шлях до папки з DLL збірками
        string path = @"D:\прога_2.1\лаб_9\dll";

        // Отримати всі DLL файли в папці
        string[] dllFileNames = Directory.GetFiles(path, "*.dll");

        foreach (var dllFile in dllFileNames)
        {
            // Завантажити збірку
            Assembly assembly = Assembly.LoadFrom(dllFile);

            // Отримати всі типи в збірці
            Type[] types = assembly.GetTypes();

            foreach (var type in types)
            {
                // Перевірити, чи реалізує тип інтерфейс IPlugin
                if (type.GetInterface("IPlugin") != null)
                {
                    // Створити екземпляр типу
                    var instance = Activator.CreateInstance(type) as IPlugin;

                    if (instance != null)
                    {
                        // Викликати метод Execute
                        double result = instance.Execute(5, 3);
                        Console.WriteLine($"Result of {type.Name}.Execute: {result}");
                    }
                }
            }
        }
    }
}
