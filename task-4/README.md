# Task 4 - Island counter

Counts islands in a grid of 1s (land) and 0s (water) using flood fill. Two land cells are part of the same island if they touch, either only up/down/left/right (4-way) or also diagonally (8-way).

What's in `island_counter.py`:
- BFS flood fill with a queue (`collections.deque`)
- DFS flood fill with a stack, so big grids don't hit the recursion limit
- recursive DFS, simpler but only for small grids
- `label_islands` gives each island its own number 1, 2, 3... and returns the size of each one
- `stats` gives number of islands, land/water cells, largest, smallest and average island
- the grid is stored as a numpy array and checked to only contain 0 and 1

## Complexity
| method | time | extra space |
|---|---|---|
| BFS | O(M*N) | O(M*N) worst case for the queue |
| DFS (stack) | O(M*N) | O(M*N) |
| DFS (recursive) | O(M*N) | O(M*N) call stack |

Every cell gets visited once at most, so it's linear in the number of cells.

## Run
```
python island_counter.py
```

## Output
```
# # . . . #
# # . . . .
. . # . # #
. . . # # .
# . . . . .

bfs      4-way: 5   8-way: 3
dfs      4-way: 5   8-way: 3
dfs_rec  4-way: 5   8-way: 3
```
