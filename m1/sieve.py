from math import isqrt


def segmented_sieve(a: int, b: int) -> list[int]:
    """Return primes in inclusive interval [a,b].

    Pure oracle implementation. No model-facing code should call this during
    training/evaluation after manifest freeze.
    """
    if b < 2 or b < a:
        return []

    a = max(a, 2)
    limit = isqrt(b) + 1

    base = [True] * (limit + 1)
    primes = []

    for p in range(2, limit + 1):
        if base[p]:
            primes.append(p)
            for k in range(p * p, limit + 1, p):
                base[k] = False

    window = [True] * (b - a + 1)

    for p in primes:
        start = max(p * p, ((a + p - 1) // p) * p)
        for k in range(start, b + 1, p):
            window[k - a] = False

    return [a + i for i, keep in enumerate(window) if keep]


def prime_count(a: int, b: int) -> int:
    return len(segmented_sieve(a, b))
