using System;
using System.Linq;
using BenchmarkDotNet.Attributes;
using BenchmarkDotNet.Running;

public class Program
{
    static void Main(string[] args)
    {
        var summary = BenchmarkRunner.Run<Benchmark>();
    }
}

public class Benchmark
{
    private int[] numbers;

    [GlobalSetup]
    public void Setup()
    {
        var random = new Random();
        numbers = Enumerable.Range(1, 1000000).Select(_ => random.Next(0, 100)).ToArray();
    }

    [Benchmark]
    public void LinqTest()
    {
        var squares = numbers.Select(x => x * x).ToArray();
    }

    [Benchmark]
    public void PlinqTest()
    {
        var squares = numbers.AsParallel().Select(x => x * x).ToArray();
    }
}
//dotnet run -c Release