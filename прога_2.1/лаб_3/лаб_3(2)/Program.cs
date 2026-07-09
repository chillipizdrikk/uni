using System;
using BenchmarkDotNet.Attributes;
using BenchmarkDotNet.Running;

public class BigInteger
{
    private readonly string value;

    public BigInteger(string value)
    {
        this.value = value;
    }

    public string Value => value;

    public static BigInteger operator +(BigInteger a, BigInteger b)
    {
        try
        {
            return new BigInteger((long.Parse(a.Value) + long.Parse(b.Value)).ToString());
        }
        catch (FormatException)
        {
            throw new InvalidOperationException("One or both BigInteger values are not valid long integers.");
        }
    }

    public static BigInteger operator -(BigInteger a, BigInteger b)
    {
        try
        {
            return new BigInteger((long.Parse(a.Value) - long.Parse(b.Value)).ToString());
        }
        catch (FormatException)
        {
            throw new InvalidOperationException("One or both BigInteger values are not valid long integers.");
        }
    }

    public static BigInteger operator *(BigInteger a, BigInteger b)
    {
        try
        {
            return new BigInteger((long.Parse(a.Value) * long.Parse(b.Value)).ToString());
        }
        catch (FormatException)
        {
            throw new InvalidOperationException("One or both BigInteger values are not valid long integers.");
        }
    }

    public static BigInteger operator /(BigInteger a, BigInteger b)
    {
        try
        {
            return new BigInteger((long.Parse(a.Value) / long.Parse(b.Value)).ToString());
        }
        catch (FormatException)
        {
            throw new InvalidOperationException("One or both BigInteger values are not valid long integers.");
        }
        catch (DivideByZeroException)
        {
            throw new DivideByZeroException("Division by zero error.");
        }
    }

    public static bool operator >(BigInteger a, BigInteger b)
    {
        return long.Parse(a.Value) > long.Parse(b.Value);
    }

    public static bool operator <(BigInteger a, BigInteger b)
    {
        return long.Parse(a.Value) < long.Parse(b.Value);
    }

    public static bool operator ==(BigInteger a, BigInteger b)
    {
        return a.Value == b.Value;
    }

    public static bool operator !=(BigInteger a, BigInteger b)
    {
        return a.Value != b.Value;
    }

    public override string ToString()
    {
        return value;
    }
}

public class Benchmark
{
    private readonly BigInteger bigInt1 = new BigInteger("123456789012345678901234567890");
    private readonly BigInteger bigInt2 = new BigInteger("987654321098765432109876543210");

    [Benchmark]
    public BigInteger AdditionBenchmark()
    {
        return bigInt1 + bigInt2;
    }

    [Benchmark]
    public BigInteger SubtractionBenchmark()
    {
        return bigInt1 - bigInt2;
    }

    [Benchmark]
    public BigInteger MultiplicationBenchmark()
    {
        return bigInt1 * bigInt2;
    }

    [Benchmark]
    public BigInteger DivisionBenchmark()
    {
        return bigInt1 / bigInt2;
    }
}

class Program
{
    static void Main(string[] args)
    {
        var summary = BenchmarkRunner.Run<Benchmark>();
    }
}
