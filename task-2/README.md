# Task 2 - Sorting benchmark

Compares four ways of sorting:
1. insertion sort - O(n^2)
2. merge sort - O(n log n)
3. quick sort with a random pivot so sorted input doesn't make it O(n^2)
4. python's `sorted()` (Timsort, written in C)

Each one runs on random, sorted and reversed data with n from 1,000 up to 100,000. Insertion sort is skipped above 10,000 on random and reversed data because it takes way too long. Every result is checked against `sorted()` so we know the sort is right.

The graph uses log scale on both axes and is saved as `benchmark_plot.png`.

```
python benchmark.py
```

What I saw: `sorted()` wins everywhere by a lot, merge and quick are close to each other, and insertion sort is only fast when the data is already sorted.
