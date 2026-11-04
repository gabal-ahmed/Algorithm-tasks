import random
import sys
import time

import matplotlib.pyplot as plt

sys.setrecursionlimit(10000)


def insertion_sort(data):
    a = data[:]
    for i in range(1, len(a)):
        x = a[i]
        j = i
        while j > 0 and a[j - 1] > x:
            a[j] = a[j - 1]
            j -= 1
        a[j] = x
    return a


def merge_sort(data):
    if len(data) <= 1:
        return data[:]
    m = len(data) // 2
    left, right = merge_sort(data[:m]), merge_sort(data[m:])
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def quick_sort(data):
    if len(data) <= 1:
        return data[:]
    pivot = random.choice(data)
    smaller = [x for x in data if x < pivot]
    equal = [x for x in data if x == pivot]
    bigger = [x for x in data if x > pivot]
    return quick_sort(smaller) + equal + quick_sort(bigger)


def builtin_sort(data):
    return sorted(data)


ALGOS = {
    "insertion": insertion_sort,
    "merge": merge_sort,
    "quick": quick_sort,
    "sorted()": builtin_sort,
}

INSERTION_LIMIT = 10000


def generate(kind, n):
    nums = [random.randint(0, 10**6) for _ in range(n)]
    if kind == "sorted":
        nums.sort()
    elif kind == "reversed":
        nums.sort(reverse=True)
    return nums


def measure(fn, data):
    t = time.perf_counter()
    out = fn(data)
    elapsed = time.perf_counter() - t
    assert out == sorted(data)
    return elapsed


def run():
    sizes = [1000, 2000, 5000, 10000, 20000, 50000, 100000]
    kinds = ["random", "sorted", "reversed"]
    results = {k: {name: [] for name in ALGOS} for k in kinds}

    for kind in kinds:
        print(f"\n{kind} data")
        print(f"{'n':>7}" + "".join(f"{name:>12}" for name in ALGOS))
        for n in sizes:
            data = generate(kind, n)
            line = f"{n:>7}"
            for name, fn in ALGOS.items():
                if name == "insertion" and n > INSERTION_LIMIT and kind != "sorted":
                    results[kind][name].append(None)
                    line += f"{'skip':>12}"
                    continue
                sec = measure(fn, data)
                results[kind][name].append(sec)
                line += f"{sec:>11.4f}s"
            print(line)

    fig, axes = plt.subplots(1, 3, figsize=(17, 5), sharey=True)
    for ax, kind in zip(axes, kinds):
        for name in ALGOS:
            pts = [(n, t) for n, t in zip(sizes, results[kind][name]) if t is not None]
            xs, ys = zip(*pts)
            ax.plot(xs, ys, marker="o", label=name)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_title(f"{kind} input")
        ax.set_xlabel("n")
        ax.grid(True, which="both", alpha=0.3)
    axes[0].set_ylabel("seconds")
    axes[0].legend()
    fig.suptitle("Sorting benchmark")
    fig.tight_layout()
    fig.savefig("benchmark_plot.png", dpi=150)
    print("\nplot saved to benchmark_plot.png")


if __name__ == "__main__":
    run()
