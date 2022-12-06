from math import sqrt, floor

from itertools import combinations


def get_max_len(total):
    return (- 1 + floor(sqrt(1 + 8 * total))) // 2


def generate_asymmetric_stars(n):
    if n < 7:
        return []
    max_len = get_max_len(n - 1)
    min_len = 3
    correct = [[] for _ in range(max_len - min_len + 1)]
    for i in range(min_len, max_len + 1):
        for comb in combinations(range(1, n), i):
            if sum(comb) == n - 1:
                correct[i - min_len].append(comb)
    print(correct)


if __name__ == '__main__':
    # for i in range(7, 35):
    #     generate_asymmetric_stars(i)
    generate_asymmetric_stars(13)
