```

BenchmarkDotNet v0.13.12, Windows 11 (10.0.22631.3593/23H2/2023Update/SunValley3)
Intel Core i7-1065G7 CPU 1.30GHz, 1 CPU, 8 logical and 4 physical cores
.NET SDK 8.0.105
  [Host]     : .NET 6.0.9 (6.0.922.41905), X64 RyuJIT AVX2
  DefaultJob : .NET 6.0.9 (6.0.922.41905), X64 RyuJIT AVX2


```
| Method    | Mean      | Error     | StdDev    |
|---------- |----------:|----------:|----------:|
| LinqTest  |  4.029 ms | 0.0803 ms | 0.1488 ms |
| PlinqTest | 10.173 ms | 0.2026 ms | 0.5878 ms |
