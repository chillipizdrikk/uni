using hw6_2;
using System;
using System.Collections;
using System.Collections.Generic;

namespace hw6_2
{
    public class CustomCollection<T> : IEnumerable<T>
    {
        private T[] items;

        public CustomCollection(T[] items)
        {
            this.items = items;
        }

        public T this[int index]
        {
            get => items[index];
            set => items[index] = value;
        }

        public CustomCollection() : this(Array.Empty<T>()) { }

        public IEnumerator<T> GetEnumerator()
        {
            return new CustomEnumerator<T>(items);
        }

        IEnumerator IEnumerable.GetEnumerator()
        {
            return GetEnumerator();
        }

        public void Add(T item)
        {
            Array.Resize(ref items, items.Length + 1);
            items[items.Length - 1] = item;
        }

    }


    public class CustomEnumerator<T> : IEnumerator<T>
    {
        private readonly T[] items;
        private int _currentIndex = -2;
        private bool doneEven = false;

        public CustomEnumerator(T[] items)
        {
            this.items = items;
        }

        public T Current => items[_currentIndex];

        object IEnumerator.Current => Current;

        public bool MoveNext()
        {
            do
            {
                _currentIndex++;
                if (_currentIndex >= items.Length && !doneEven)
                {
                    _currentIndex = -1;
                    doneEven = true;
                }
            }
            while (_currentIndex < items.Length && _currentIndex % 2 != (doneEven ? 1 : 0));

            return _currentIndex < items.Length;
        }

        public void Reset()
        {
            _currentIndex = doneEven ? -1 : -2;
        }

        public void Dispose() { }
    }
    public class Animal
    {
        private string Name { get; set; }
        private string Type { get; set; }

        public Animal(string name, string type)
        {
            Name = name;
            Type = type;
        }

        public override string ToString()
        {
            return $"{Name} is {Type}!";
        }
    }
    public abstract class Program
    {
        public static void Main(string[] args)
        {
            var animals = new CustomCollection<Animal>();
            animals.Add(new Animal("Dog", "Mammal"));
            animals.Add(new Animal("Cat", "Mammal"));
            animals.Add(new Animal("Parrot", "Bird"));
            animals.Add(new Animal("Snake", "Reptile"));
            animals.Add(new Animal("Fish", "Fish"));
            //animals.Add(new Animal("Spider", "Arachnid"));
            animals.Add(new Animal("Ant", "Insect"));
            animals.Add(new Animal("Frog", "Amphibian"));
            animals.Add(new Animal("Turtle", "Reptile"));
            animals.Add(new Animal("Dolphin", "Mammal"));

            Console.WriteLine("\nТварини в порядку, в якому вони були додані:\n");
            for (int i = 0; i < animals.ToArray().Length; i++)
            {
                Console.WriteLine($" {i}: {animals[i]}");
            }



            Console.WriteLine("\nТварини в порядку, визначеному CustomEnumerator:\n");
            foreach (var animal in animals)
            {
                Console.WriteLine(animal);
            }
        }
    }

}