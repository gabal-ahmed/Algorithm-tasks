import os
import random
import time

import matplotlib.pyplot as plt

from insertion_sort import insertion_sort


def merge_sort(a):
    if len(a) < 2:
        return a
    half = len(a) // 2
    l = merge_sort(a[:half])
    r = merge_sort(a[half:])
    out = []
    i, j = 0, 0
    while i < len(l) and j < len(r):
        if l[i] <= r[j]:
            out.append(l[i])
            i += 1
        else:
            out.append(r[j])
            j += 1
    return out + l[i:] + r[j:]


def timed(fn, data):
    start = time.perf_counter()
    res = fn(data)
    return (time.perf_counter() - start) * 1000, res


def make_input(kind, n):
    if kind == "sorted":
        return list(range(n))
    if kind == "reversed":
        return list(range(n, 0, -1))
    return [random.randint(1, 10**5) for _ in range(n)]


def main():
    sizes = [100, 500, 1000, 1500, 2000, 2500, 3000, 4000, 5000]
    kinds = ["sorted", "random", "reversed"]
    runs = 3

    times = {k: [] for k in kinds}
    comps = {k: [] for k in kinds}
    shifts = {k: [] for k in kinds}
    merge_times = []

    print("n".rjust(6), *(k.rjust(12) for k in kinds), "merge".rjust(10))
    for n in sizes:
        row = []
        for kind in kinds:
            t_sum = c_sum = s_sum = 0
            for _ in range(runs):
                ms, (_, c, s) = timed(insertion_sort, make_input(kind, n))
                t_sum += ms
                c_sum += c
                s_sum += s
            times[kind].append(t_sum / runs)
            comps[kind].append(c_sum / runs)
            shifts[kind].append(s_sum / runs)
            row.append(t_sum / runs)

        ms, _ = timed(merge_sort, make_input("random", n))
        merge_times.append(ms)

        print(str(n).rjust(6), *(f"{x:12.3f}" for x in row), f"{ms:10.3f}")

    os.makedirs("plots", exist_ok=True)
    fig, (left, right) = plt.subplots(1, 2, figsize=(14, 5.5))

    colors = {"sorted": "green", "random": "tab:blue", "reversed": "tab:red"}
    for kind in kinds:
        left.plot(sizes, times[kind], marker="o", color=colors[kind], label=f"insertion ({kind})")
    left.plot(sizes, merge_times, marker="x", linestyle="--", color="purple", label="merge sort (random)")

    big = sizes[-1]
    c2 = times["reversed"][-1] / big ** 2
    c1 = times["sorted"][-1] / big
    left.plot(sizes, [c2 * n * n for n in sizes], ":", color="black", label="~ n^2")
    left.plot(sizes, [c1 * n for n in sizes], ":", color="gray", label="~ n")
    left.set_title("Running time")
    left.set_xlabel("n")
    left.set_ylabel("ms")
    left.grid(alpha=0.4)
    left.legend()

    for kind in kinds:
        right.plot(sizes, comps[kind], marker="o", color=colors[kind], label=f"{kind} comparisons")
        right.plot(sizes, shifts[kind], linestyle="--", color=colors[kind], label=f"{kind} shifts")
    right.set_title("Comparisons and shifts")
    right.set_xlabel("n")
    right.set_ylabel("count")
    right.grid(alpha=0.4)
    right.legend()

    fig.tight_layout()
    path = os.path.join("plots", "insertion_sort_analysis.png")
    fig.savefig(path, dpi=150)
    print("saved", path)

    print("\nn = 5000 counts:")
    for kind in kinds:
        print(f"  {kind:9} comparisons={comps[kind][-1]:.0f} shifts={shifts[kind][-1]:.0f}")


if __name__ == "__main__":
    main()
