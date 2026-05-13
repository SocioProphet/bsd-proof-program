from pathlib import Path

from m1.sieve import segmented_sieve, prime_count
from m1.zero_table import validate_zero_table


def test_segmented_sieve_small_interval():
    assert segmented_sieve(10, 30) == [11, 13, 17, 19, 23, 29]


def test_prime_count_reference_window():
    # pi(10000)=1229, pi(20000)=2262
    assert prime_count(10000, 20000) == 1033


def test_zero_table_validation(tmp_path: Path):
    vals = [
        14.134725141734693790,
    ]

    while len(vals) < 49:
        vals.append(vals[-1] + 1.0)

    vals.append(143.111845807620632739)

    while len(vals) < 99:
        vals.append(vals[-1] + 1.0)

    vals.append(236.524229665816205802)

    while len(vals) < 199:
        vals.append(vals[-1] + 1.0)

    vals.append(396.381854222592186931)

    while len(vals) < 250:
        vals.append(vals[-1] + 1.0)

    p1 = tmp_path / "primary.txt"
    p2 = tmp_path / "secondary.txt"

    payload = "\n".join(str(v) for v in vals)

    p1.write_text(payload)
    p2.write_text(payload)

    meta = validate_zero_table(p1, p2)

    assert meta.count == 250
    assert len(meta.sha256) == 64
