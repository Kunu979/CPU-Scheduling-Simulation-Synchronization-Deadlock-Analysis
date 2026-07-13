import threading

# ---------------------------------------------------
# Unsynchronized Version (Deterministic Race Condition)
# ---------------------------------------------------

counter = 0
barrier = threading.Barrier(2)


def race_increment(thread_name):
    global counter

    print(f"{thread_name} reading counter...")

    temp = counter          # Read shared value

    # Force both threads to read before either writes
    barrier.wait()

    temp = temp + 1         # Modify local copy

    counter = temp          # Write back

    print(f"{thread_name} wrote {counter}")


def run_unsynchronized():

    global counter
    counter = 0

    print("=" * 60)
    print("UNSYNCHRONIZED VERSION")
    print("=" * 60)

    t1 = threading.Thread(target=race_increment, args=("Thread-1",))
    t2 = threading.Thread(target=race_increment, args=("Thread-2",))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("\nExpected Counter : 2")
    print("Actual Counter   :", counter)

    if counter != 2:
        print("Race condition detected!")
    else:
        print("No race detected.")


# ---------------------------------------------------
# Synchronized Version (Binary Semaphore / Lock)
# ---------------------------------------------------

counter = 0
lock = threading.Lock()


def safe_increment(thread_name):
    global counter

    with lock:
        temp = counter
        temp += 1
        counter = temp

        print(f"{thread_name} updated counter to {counter}")


def run_synchronized():

    global counter
    counter = 0

    print("\n" + "=" * 60)
    print("SYNCHRONIZED VERSION")
    print("=" * 60)

    t1 = threading.Thread(target=safe_increment, args=("Thread-1",))
    t2 = threading.Thread(target=safe_increment, args=("Thread-2",))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("\nExpected Counter : 2")
    print("Actual Counter   :", counter)

    if counter == 2:
        print("Synchronization successful!")
    else:
        print("Synchronization failed.")


# ---------------------------------------------------
# Main
# ---------------------------------------------------

if __name__ == "__main__":

    run_unsynchronized()

    run_synchronized()