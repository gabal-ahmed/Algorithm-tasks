class Task:
    def __init__(self, pid, name, priority, burst, arrival=0):
        self.pid = pid
        self.name = name
        self.priority = priority
        self.burst = burst
        self.arrival = arrival
        self.start = None
        self.finish = None

    def __repr__(self):
        return f"Task({self.pid}, {self.name!r}, p={self.priority})"


class MaxHeap:
    def __init__(self):
        self.items = []

    def __len__(self):
        return len(self.items)

    def _bigger(self, a, b):
        x, y = self.items[a], self.items[b]
        if x.priority != y.priority:
            return x.priority > y.priority
        return x.arrival < y.arrival

    def _swap(self, a, b):
        self.items[a], self.items[b] = self.items[b], self.items[a]

    def insert(self, task):
        self.items.append(task)
        i = len(self.items) - 1
        while i > 0:
            parent = (i - 1) // 2
            if not self._bigger(i, parent):
                break
            self._swap(i, parent)
            i = parent

    def peek_max(self):
        return self.items[0] if self.items else None

    def extract_max(self):
        if not self.items:
            return None
        top = self.items[0]
        last = self.items.pop()
        if self.items:
            self.items[0] = last
            self._heapify(0)
        return top

    def _heapify(self, i):
        n = len(self.items)
        while True:
            l, r = 2 * i + 1, 2 * i + 2
            best = i
            if l < n and self._bigger(l, best):
                best = l
            if r < n and self._bigger(r, best):
                best = r
            if best == i:
                return
            self._swap(i, best)
            i = best


class Scheduler:
    def __init__(self, tasks):
        self.pending = sorted(tasks, key=lambda t: t.arrival)
        self.ready = MaxHeap()
        self.clock = 0
        self.done = []

    def _admit(self):
        while self.pending and self.pending[0].arrival <= self.clock:
            t = self.pending.pop(0)
            self.ready.insert(t)
            print(f"[t={self.clock:>3}] arrived  {t.name} (priority {t.priority})")

    def run(self):
        while self.pending or len(self.ready):
            self._admit()
            if not len(self.ready):
                self.clock = self.pending[0].arrival
                continue
            t = self.ready.extract_max()
            t.start = self.clock
            print(f"[t={self.clock:>3}] running  {t.name} for {t.burst} units")
            self.clock += t.burst
            t.finish = self.clock
            self.done.append(t)
        self.report()

    def report(self):
        print(f"\n{'task':<20}{'prio':>5}{'arrive':>8}{'start':>7}{'end':>6}{'wait':>6}{'tat':>6}")
        total_wait = total_tat = 0
        for t in self.done:
            wait = t.start - t.arrival
            tat = t.finish - t.arrival
            total_wait += wait
            total_tat += tat
            print(f"{t.name:<20}{t.priority:>5}{t.arrival:>8}{t.start:>7}{t.finish:>6}{wait:>6}{tat:>6}")
        n = len(self.done)
        print(f"\naverage waiting time:    {total_wait / n:.2f}")
        print(f"average turnaround time: {total_tat / n:.2f}")


def heap_check():
    h = MaxHeap()
    for i, p in enumerate([5, 1, 9, 3, 7, 9, 2]):
        h.insert(Task(i, f"t{i}", p, 1))
    print("peek:", h.peek_max())
    order = []
    while len(h):
        order.append(h.extract_max().priority)
    print("extract order:", order)
    assert order == sorted(order, reverse=True)


if __name__ == "__main__":
    heap_check()
    print()

    workload = [
        Task(1, "Backup", 10, 6, 0),
        Task(2, "Music Player", 50, 3, 1),
        Task(3, "Mouse Click", 90, 1, 2),
        Task(4, "Antivirus Scan", 30, 5, 2),
        Task(5, "System Update", 20, 4, 4),
        Task(6, "Keyboard Input", 85, 1, 7),
        Task(7, "Video Render", 40, 8, 20),
    ]
    Scheduler(workload).run()
