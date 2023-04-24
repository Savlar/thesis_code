import time


def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n - 2) + fib(n - 1)

size = 45
times = [[] for _ in range(size)]
for i in range(size):
    for _ in range(5):
        start = time.time()
        fib(i)
        times[i].append(time.time() - start)
for n, t in enumerate(times):
    print(n, sum(t) / len(t))
