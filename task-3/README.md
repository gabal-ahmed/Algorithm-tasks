# Task 3 - OS task scheduler with a max heap

A small simulation of a priority CPU scheduler. The ready queue is a binary max heap that I wrote using a plain list (no `heapq`).

Heap operations:
- `insert` - O(log n)
- `extract_max` - O(log n), gives the task with the highest priority
- `peek_max` - O(1)

If two tasks have the same priority the one that arrived first goes first.

The scheduler is non-preemptive: every time the CPU is free it takes the highest priority task that has arrived and runs it until its burst finishes. At the end it prints start/end times, waiting time and turnaround time for every task and the averages.

Everything is in `task_scheduler.py`.

```
python task_scheduler.py
```
