using BenchmarkDotNet.Attributes;
using BenchmarkDotNet.Running;
using System;
using System.Collections.Generic;

namespace BenchmarkExample
{
    public class CustomStack<T>
    {
        private T[] _items = Array.Empty<T>();
        private int _size = -1;
        private int _capacity;

        public void Push(T item)
        {
            if (_size == _capacity - 1)
            {
                _capacity = _capacity == 0 ? 4 : _capacity * 2;

                var newItems = new T[_capacity];
                for (var i = 0; i <= _size; i++)
                {
                    newItems[i] = _items[i];
                }
                _items = newItems;
            }
            _items[++_size] = item;
        }

        public T Pop()
        {
            if (_size == -1)
            {
                throw new InvalidOperationException("Stack is empty");
            }
            return _items[_size--];
        }

        public T Peek()
        {
            if (_size == -1)
            {
                throw new InvalidOperationException("Stack is empty");
            }
            return _items[_size];
        }

        public bool IsEmpty()
        {
            return _size == -1;
        }

        public int Contains(T item)
        {
            for (var i = 0; i <= _size; i++)
            {
                if (_items[i]!.Equals(item))
                {
                    return i;
                }
            }
            return -1;
        }

        public void Clear()
        {
            _size = -1;
        }

        public int Size()
        {
            return _size + 1; // Розмір стеку - це _size + 1
        }

        public void Print()
        {
            Console.Write("[");
            for (var i = 0; i <= _size; i++)
            {
                Console.Write(_items[i]);
                if (i < _size)
                {
                    Console.Write(", ");
                }
            }
            Console.WriteLine("]");
        }


    }

    public class CustomStackVsSystemStackBenchmark
    {
        private const int N = 10000;
        private readonly int[] data = new int[N];
        private readonly CustomStack<int> customStack = new CustomStack<int>();
        private readonly Stack<int> systemStack = new Stack<int>();

        public CustomStackVsSystemStackBenchmark()
        {
            // Заповнення даних для бенчмарків
            for (int i = 0; i < N; i++)
            {
                data[i] = i;
                customStack.Push(i);
                systemStack.Push(i);
            }
        }

        [Benchmark]
        public int CustomStack_Push()
        {
            for (int i = 0; i < N; i++)
            {
                customStack.Push(i);
            }
            return customStack.Size(); // Повертаємо значення _size
        }

        [Benchmark]
        public int SystemStack_Push()
        {
            for (int i = 0; i < N; i++)
            {
                systemStack.Push(i);
            }
            return systemStack.Count;
        }

        [Benchmark]
        public int CustomStack_Peek()
        {
            int sum = 0;
            for (int i = 0; i < N; i++)
            {
                sum += customStack.Peek();
            }
            return sum;
        }

        [Benchmark]
        public int SystemStack_Peek()
        {
            int sum = 0;
            for (int i = 0; i < N; i++)
            {
                sum += systemStack.Peek();
            }
            return sum;
        }

        [Benchmark]
        public bool CustomStack_Contains()
        {
            bool found = false;
            for (int i = 0; i < N; i++)
            {
                found = customStack.Contains(i) != -1;
            }
            return found;
        }


        [Benchmark]
        public int SystemStack_Contains()
        {
            int sum = 0;
            for (int i = 0; i < N; i++)
            {
                sum += systemStack.Contains(i) ? 1 : 0;
            }
            return sum;
        }

        public void RunBenchmark()
        {
            var summary = BenchmarkRunner.Run<CustomStackVsSystemStackBenchmark>();
        }
    }

    public abstract class Program3
    {
        public static void Main(string[] args)
        {
            var stack = new CustomStack<int>();

            stack.Push(1);
            stack.Push(2);
            stack.Push(5);
            stack.Push(7);

            stack.Print();

            var contains5 = stack.Contains(5);
            Console.WriteLine(contains5);

            var peek = stack.Peek();
            Console.WriteLine(peek);

            stack.Pop();
            stack.Print();

            var benchmark = new CustomStackVsSystemStackBenchmark();
            benchmark.RunBenchmark();
        }
    }
}
//dotnet run -c Release