from collections import deque

class Process:
    def __init__(self, pid, arrival, burst):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst


# Dataset (5 processes)
processes = [
    Process("P1", 0, 5),
    Process("P2", 1, 3),
    Process("P3", 2, 8),
    Process("P4", 3, 6),
    Process("P5", 4, 2)
]


def print_results(title, waiting, turnaround):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    total_wait = 0
    total_turn = 0

    print("{:<5} {:<10} {:<12}".format("PID", "Waiting", "Turnaround"))

    for pid in waiting:
        print("{:<5} {:<10} {:<12}".format(
            pid,
            waiting[pid],
            turnaround[pid]
        ))
        total_wait += waiting[pid]
        total_turn += turnaround[pid]

    n = len(waiting)

    print("\nAverage Waiting Time :", round(total_wait / n, 2))
    print("Average Turnaround Time :", round(total_turn / n, 2))


###################################################
# FCFS
###################################################

def fcfs(processes):

    time = 0
    waiting = {}
    turnaround = {}

    plist = sorted(
        enumerate(processes),
        key=lambda x: (x[1].arrival, x[0])
    )

    for _, p in plist:

        if time < p.arrival:
            time = p.arrival

        waiting[p.pid] = time - p.arrival

        time += p.burst

        turnaround[p.pid] = waiting[p.pid] + p.burst

    print_results("FCFS", waiting, turnaround)


###################################################
# SJF (Non Preemptive)
###################################################

def sjf(processes):

    n = len(processes)

    completed = 0
    current = 0

    waiting = {}
    turnaround = {}

    visited = [False] * n

    while completed < n:

        ready = []

        for i, p in enumerate(processes):

            if not visited[i] and p.arrival <= current:
                ready.append((p.burst, p.arrival, i, p))

        if len(ready) == 0:
            current += 1
            continue

        ready.sort()

        burst, arrival, index, p = ready[0]

        visited[index] = True

        waiting[p.pid] = current - arrival

        current += burst

        turnaround[p.pid] = waiting[p.pid] + burst

        completed += 1

    print_results("Shortest Job First", waiting, turnaround)


###################################################
# Round Robin
###################################################

def round_robin(processes, quantum):

    n = len(processes)

    remaining = {}

    waiting = {}

    turnaround = {}

    completion = {}

    for p in processes:
        remaining[p.pid] = p.burst

    time = 0

    queue = deque()

    arrived = set()

    while len(completion) < n:

        # enqueue newly arrived processes
        for p in processes:
            if p.arrival <= time and p.pid not in arrived:
                queue.append(p)
                arrived.add(p.pid)

        if not queue:
            time += 1
            continue

        p = queue.popleft()

        execute = min(quantum, remaining[p.pid])

        start = time

        time += execute

        remaining[p.pid] -= execute

        # enqueue arrivals during execution BEFORE requeue
        for proc in processes:
            if start < proc.arrival <= time and proc.pid not in arrived:
                queue.append(proc)
                arrived.add(proc.pid)

        if remaining[p.pid] > 0:
            queue.append(p)
        else:
            completion[p.pid] = time

    for p in processes:

        turnaround[p.pid] = completion[p.pid] - p.arrival

        waiting[p.pid] = turnaround[p.pid] - p.burst

    print_results(
        f"Round Robin (Quantum={quantum})",
        waiting,
        turnaround
    )


###################################################
# MAIN
###################################################

fcfs(processes)

sjf(processes)

round_robin(processes, quantum=2)