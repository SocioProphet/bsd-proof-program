from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path

from m1.psi_residual import ResidualResult


@dataclass(frozen=True)
class BoxRecord:
    left: int | float
    right: int | float
    prime_count: int
    psi_increment: float


@dataclass(frozen=True)
class Manifest:
    interval: tuple[int | float, int | float]
    resolution_du: float
    zero_table_sha256: str
    boxes: list[BoxRecord]
    residuals: list[ResidualResult]


class FrozenManifestWriter:
    """Writes immutable benchmark manifests.

    After manifest emission, evaluation/model layers must not invoke the sieve.
    """

    @staticmethod
    def write(path: str | Path, manifest: Manifest) -> str:
        payload = {
            "interval": list(manifest.interval),
            "resolution_du": manifest.resolution_du,
            "zero_table_sha256": manifest.zero_table_sha256,
            "boxes": [asdict(x) for x in manifest.boxes],
            "residuals": [asdict(x) for x in manifest.residuals],
        }

        text = json.dumps(payload, indent=2, sort_keys=True)
        digest = sha256(text.encode("utf-8")).hexdigest()

        wrapped = {
            "manifest_sha256": digest,
            "payload": payload,
        }

        Path(path).write_text(json.dumps(wrapped, indent=2, sort_keys=True))
        return digest
