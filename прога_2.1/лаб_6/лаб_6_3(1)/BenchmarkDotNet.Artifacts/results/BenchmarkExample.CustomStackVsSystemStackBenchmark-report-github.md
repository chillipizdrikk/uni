```

BenchmarkDotNet v0.13.12, Windows 11 (10.0.22631.3447/23H2/2023Update/SunValley3)
Intel Core i7-1065G7 CPU 1.30GHz, 1 CPU, 8 logical and 4 physical cores
.NET SDK 8.0.104
  [Host]     : .NET 6.0.9 (6.0.922.41905), X64 RyuJIT AVX2
  DefaultJob : .NET 6.0.9 (6.0.922.41905), X64 RyuJIT AVX2


```
| Method               | Mean           | Error         | StdDev        | Median         |
|--------------------- |---------------:|--------------:|--------------:|---------------:|
| CustomStack_Push     |             NA |            NA |            NA |             NA |
| SystemStack_Push     |             NA |            NA |            NA |             NA |
| CustomStack_Peek     |      17.782 μs |     0.5769 μs |     1.6736 μs |      16.819 μs |
| SystemStack_Peek     |       7.594 μs |     0.1065 μs |     0.0889 μs |       7.568 μs |
| CustomStack_Contains | 178,068.862 μs | 3,138.2227 μs | 3,613.9819 μs | 177,703.167 μs |
| SystemStack_Contains |  14,518.022 μs |   184.6669 μs |   172.7375 μs |  14,475.117 μs |

Benchmarks with issues:
  CustomStackVsSystemStackBenchmark.CustomStack_Push: DefaultJob
  CustomStackVsSystemStackBenchmark.SystemStack_Push: DefaultJob
