```

BenchmarkDotNet v0.13.12, Windows 11 (10.0.22631.3447/23H2/2023Update/SunValley3)
Intel Core i7-1065G7 CPU 1.30GHz, 1 CPU, 8 logical and 4 physical cores
.NET SDK 8.0.104
  [Host]     : .NET 6.0.9 (6.0.922.41905), X64 RyuJIT AVX2
  DefaultJob : .NET 6.0.9 (6.0.922.41905), X64 RyuJIT AVX2


```
| Method                       | Mean     | Error     | StdDev    |
|----------------------------- |---------:|----------:|----------:|
| Add_SystemDictionary         |       NA |        NA |        NA |
| Add_CustomDictionary         |       NA |        NA |        NA |
| Remove_SystemDictionary      | 6.102 ns | 0.1306 ns | 0.1222 ns |
| Remove_CustomDictionary      | 3.770 ns | 0.1090 ns | 0.1993 ns |
| ContainsKey_SystemDictionary | 6.666 ns | 0.1221 ns | 0.1020 ns |
| ContainsKey_CustomDictionary | 1.505 ns | 0.0598 ns | 0.0559 ns |
| Indexer_SystemDictionary     |       NA |        NA |        NA |
| Indexer_CustomDictionary     |       NA |        NA |        NA |

Benchmarks with issues:
  Benchmark.Add_SystemDictionary: DefaultJob
  Benchmark.Add_CustomDictionary: DefaultJob
  Benchmark.Indexer_SystemDictionary: DefaultJob
  Benchmark.Indexer_CustomDictionary: DefaultJob
