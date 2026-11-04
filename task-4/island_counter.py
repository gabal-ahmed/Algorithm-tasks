from collections import deque

import numpy as np

NEIGHBORS = {
    4: [(-1, 0), (1, 0), (0, -1), (0, 1)],
    8: [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)],
}


def to_grid(data):
    grid = np.array(data, dtype=int)
    if grid.ndim != 2:
        raise ValueError("grid has to be 2D")
    if not np.isin(grid, (0, 1)).all():
        raise ValueError("grid can only have 0 and 1")
    return grid


def flood(grid, labels, start, label, moves, use_queue):
    rows, cols = grid.shape
    frontier = deque([start])
    labels[start] = label
    size = 0
    while frontier:
        r, c = frontier.popleft() if use_queue else frontier.pop()
        size += 1
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 1 and labels[nr, nc] == 0:
                labels[nr, nc] = label
                frontier.append((nr, nc))
    return size


def flood_recursive(grid, labels, r, c, label, moves):
    rows, cols = grid.shape
    labels[r, c] = label
    size = 1
    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 1 and labels[nr, nc] == 0:
            size += flood_recursive(grid, labels, nr, nc, label, moves)
    return size


def label_islands(data, method="bfs", connectivity=4):
    if connectivity not in NEIGHBORS:
        raise ValueError("connectivity must be 4 or 8")
    if method not in ("bfs", "dfs", "dfs_rec"):
        raise ValueError("method must be bfs, dfs or dfs_rec")

    grid = to_grid(data)
    moves = NEIGHBORS[connectivity]
    labels = np.zeros_like(grid)
    sizes = {}
    count = 0

    for r, c in zip(*np.nonzero(grid)):
        if labels[r, c]:
            continue
        count += 1
        if method == "dfs_rec":
            sizes[count] = flood_recursive(grid, labels, r, c, count, moves)
        else:
            sizes[count] = flood(grid, labels, (r, c), count, moves, method == "bfs")

    return count, labels, sizes


def count_islands(data, method="bfs", connectivity=4):
    return label_islands(data, method, connectivity)[0]


def stats(data, connectivity=4):
    grid = to_grid(data)
    count, _, sizes = label_islands(grid, connectivity=connectivity)
    areas = list(sizes.values())
    return {
        "islands": count,
        "land": int(grid.sum()),
        "water": int(grid.size - grid.sum()),
        "largest": max(areas, default=0),
        "smallest": min(areas, default=0),
        "average": round(float(np.mean(areas)), 2) if areas else 0.0,
    }


def show(grid):
    for row in grid:
        print(" ".join("#" if x else "." for x in row))


if __name__ == "__main__":
    world = [
        [1, 1, 0, 0, 0, 1],
        [1, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 1],
        [0, 0, 0, 1, 1, 0],
        [1, 0, 0, 0, 0, 0],
    ]

    show(world)
    print()
    for m in ("bfs", "dfs", "dfs_rec"):
        print(f"{m:8} 4-way: {count_islands(world, m, 4)}   8-way: {count_islands(world, m, 8)}")

    n, labels, sizes = label_islands(world)
    print("\nlabels (4-way):")
    print(labels)
    print("sizes:", sizes)
    print("stats:", stats(world))

    rng = np.random.default_rng(7)
    big = (rng.random((300, 300)) < 0.45).astype(int)
    a = count_islands(big, "bfs")
    b = count_islands(big, "dfs")
    print(f"\nrandom 300x300 grid -> bfs: {a}, dfs: {b}")
    assert a == b
