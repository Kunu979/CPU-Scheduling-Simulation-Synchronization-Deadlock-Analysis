# CPU-Scheduling-Simulation-Synchronization-Deadlock-Analysis

# CampusConnect - Operating Systems Assignment

## Student Information

**Project:** CampusConnect Operating Systems Simulation

---

# Scheduling Simulator

## Algorithms Implemented

* First Come First Serve (FCFS)
* Shortest Job First (SJF - Non-Preemptive)
* Round Robin (Configurable Time Quantum)

## Dataset

| Process | Arrival Time | Burst Time |
| ------- | ------------ | ---------- |
| P1      | 0            | 5          |
| P2      | 1            | 3          |
| P3      | 2            | 8          |
| P4      | 3            | 6          |
| P5      | 4            | 2          |

## Tie-Breaking Rules

* If two processes have the same arrival time, they are executed in the order they appear in the input.
* For SJF, if two processes have the same burst time, arrival time is used first, followed by process ID/input order.
* For Round Robin, when a process finishes its time quantum, all processes that arrived during that quantum are added to the ready queue before the preempted process is placed back at the end of the queue.

---

# Priority Scheduling with Aging

## Priority Convention

Higher numeric value = Higher priority.

### Initial Priorities

| Process | Priority |
| ------- | -------- |
| P1      | 10       |
| P2      | 8        |
| P3      | 2        |
| P4      | 9        |
| P5      | 7        |

### Starvation Scenario

Assume that every 2 time units, a new process with priority **10** arrives. Because higher-priority processes continue arriving, **P3 (priority 2)** never gets CPU time during the simulated period. Without aging, P3 would be starved indefinitely.

### Aging Policy

Every **5 time units**, the priority of every waiting process increases by **1**.

### Aging Trace

| Time | P3 Priority |
| ---- | ----------- |
| 0    | 2           |
| 5    | 3           |
| 10   | 4           |
| 15   | 5           |
| 20   | 6           |
| 25   | 7           |
| 30   | 8           |
| 35   | 9           |
| 40   | 10          |

After aging, P3 eventually reaches the highest priority and is scheduled, eliminating starvation.

---

# Synchronization

## Unsynchronized Version

Two threads increment a shared counter.

A `threading.Barrier` is placed **between the read and write operations**, forcing both threads to read the same value before either writes. As a result, one increment is always lost, producing an incorrect final counter value.

Example:

Expected Counter = 2

Actual Counter = 1

This demonstrates a deterministic race condition.

---

## Synchronized Version

A binary semaphore (`threading.Lock`) protects the critical section.

The Barrier is removed because mutual exclusion makes the read-modify-write operation atomic.

Example:

Expected Counter = 2

Actual Counter = 2

The race condition is eliminated.

---

# Deadlock Analysis

## Scenario

CampusConnect backend contains:

### Processes

* P1 – Report Generator
* P2 – Student Record Service
* P3 – Cache Manager

### Resources

* R1 – Database Connection
* R2 – File Lock
* R3 – Cache Lock

### Resource Allocation Graph

R1 → P1 (allocated)

P1 → R2 (requested)

R2 → P2 (allocated)

P2 → R3 (requested)

R3 → P3 (allocated)

P3 → R1 (requested)

---

## Four Necessary Conditions

### Mutual Exclusion

Each resource can be used by only one process at a time.

### Hold and Wait

Each process holds one resource while waiting for another.

### No Preemption

Resources cannot be forcibly taken away from a process.

### Circular Wait

P1 waits for P2, P2 waits for P3, and P3 waits for P1, forming a circular dependency.

---

## Breaking the Deadlock

Remove the edge:

P3 → R1 (requested)

This breaks the circular wait and allows execution to continue.

---

## Deadlock Prevention Strategy

**Resource Ordering**

Require every process to request resources in the same predefined order (R1 → R2 → R3).

### Limitation

Processes may need to request resources earlier than necessary, reducing concurrency and resource utilization.

---

# Files

* `scheduler.py` – FCFS, SJF, Round Robin scheduling simulator
* `synchronization.py` – Race condition demonstration and synchronization using a binary semaphore
* `README.md` – Scheduling rules, aging trace, synchronization explanation, and deadlock analysis

---

# Expected Results

* FCFS, SJF, and Round Robin calculate waiting time and turnaround time for every process.
* Round Robin accepts a configurable time quantum.
* Aging prevents starvation.
* Unsynchronized version produces an incorrect counter value.
* Synchronized version always produces the correct counter value.
* Deadlock scenario satisfies all four necessary conditions and demonstrates one prevention strategy.
