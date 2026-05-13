from __future__ import annotations

import math
from functools import lru_cache


def _is_prime_power(n: int) -> tuple[bool, int | None]:
    """Return (True, p) when n is a positive power of prime p."""
    if n < 2:
        return (False, None)

    # p^1 case and trial division factorization are sufficient for M1 fixtures.
    m = n
    p = None
    d = 2
    while d * d <= m:
        if m % d == 0:
            p = d
            while m % d == 0:
                m //= d
            break
        d += 1 if d == 2 else 2

    if p is None:
        return (True, n)

    if m != 1:
        return (False, None)

    # n had exactly one prime divisor p, hence is p^k.
    return (True, p)


def von_mangoldt(n: int) -> float:
    """Return Lambda(n), the von Mangoldt function."""
    ok, p = _is_prime_power(n)
    if not ok or p is None:
        return 0.0
    return math.log(p)


@lru_cache(maxsize=256)
def chebyshev_psi_floor(x_floor: int) -> float:
    """Compute psi(x)=sum_{n<=x} Lambda(n) for integer floor(x).

    This is exact up to floating log evaluation and suitable for M1 infrastructure
    fixtures. Larger runs can later swap in an audited faster engine under the
    same function boundary.
    """
    if x_floor < 2:
        return 0.0
    return sum(von_mangoldt(n) for n in range(2, x_floor + 1))


def chebyshev_psi(x: int | float) -> float:
    return chebyshev_psi_floor(math.floor(x))


def chebyshev_psi_increment(a: int | float, b: int | float) -> float:
    if b < a:
        raise ValueError("requires b >= a")
    return chebyshev_psi(b) - chebyshev_psi(a)
