```

BenchmarkDotNet v0.13.12, Windows 11 (10.0.22631.3447/23H2/2023Update/SunValley3)
Intel Core i7-1065G7 CPU 1.30GHz, 1 CPU, 8 logical and 4 physical cores
.NET SDK 8.0.104
  [Host]     : .NET 6.0.9 (6.0.922.41905), X64 RyuJIT AVX2
  DefaultJob : .NET 6.0.9 (6.0.922.41905), X64 RyuJIT AVX2


```
| Method              | Mean      | Error     | StdDev   | Median    |
|-------------------- |----------:|----------:|---------:|----------:|
| QuickSortBenchmark  | 444.87 ns | 25.446 ns | 72.60 ns | 416.57 ns |
| BubbleSortBenchmark |  58.46 ns |  3.955 ns | 11.66 ns |  53.96 ns |
