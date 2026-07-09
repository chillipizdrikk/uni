namespace hw6_3;

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


public abstract class Program
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
    }
}