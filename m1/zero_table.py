from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

# Hard fixtures from standard zeta-zero tables.
FIXTURES = {
    1: 14.134725141734693790,
    50: 143.111845807620632739,
    100: 236.524229665816205802,
    200: 396.381854222592186931,
}


@dataclass(frozen=True)
class ZeroTableMetadata:
    path: str
    count: int
    sha256: str


class ZeroTableValidationError(RuntimeError):
    pass


def _load_table(path: str | Path) -> list[float]:
    vals = []
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        vals.append(float(line.split()[0]))
    return vals


def validate_zero_table(
    table_path: str | Path,
    independent_source_path: str | Path,
    n_check: int = 200,
) -> ZeroTableMetadata:
    primary = _load_table(table_path)
    secondary = _load_table(independent_source_path)

    if len(primary) < n_check or len(secondary) < n_check:
        raise ZeroTableValidationError("insufficient zero-table length")

    for i in range(1, n_check):
        if primary[i] <= primary[i - 1]:
            raise ZeroTableValidationError("non-monotone gamma sequence")

    for idx, fixture in FIXTURES.items():
        observed = primary[idx - 1]
        if abs(observed - fixture) > 1e-9:
            raise ZeroTableValidationError(
                f"fixture mismatch gamma_{idx}: {observed} != {fixture}"
            )

    for i in range(n_check):
        if abs(primary[i] - secondary[i]) > 1e-12:
            raise ZeroTableValidationError(
                f"cross-source mismatch at index {i+1}"
            )

    digest = sha256(Path(table_path).read_bytes()).hexdigest()

    return ZeroTableMetadata(
        path=str(table_path),
        count=len(primary),
        sha256=digest,
    )
