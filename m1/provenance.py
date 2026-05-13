from __future__ import annotations

import json
import platform
import sys
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from hashlib import sha256


@dataclass(frozen=True)
class ProvenanceRecord:
    created_utc: str
    python_version: str
    platform: str
    parameters_hash: str
    spectral_source: str
    spectral_hash: str


class ProvenanceError(RuntimeError):
    pass



def canonical_hash(obj: object) -> str:
    payload = json.dumps(obj, sort_keys=True, default=str)
    return sha256(payload.encode("utf-8")).hexdigest()



def spectral_hash(gammas: list[float]) -> str:
    return canonical_hash([round(x, 15) for x in gammas])



def build_provenance_record(parameters: dict, gammas: list[float], spectral_source: str) -> ProvenanceRecord:
    if not spectral_source:
        raise ProvenanceError("spectral_source required")

    return ProvenanceRecord(
        created_utc=datetime.now(UTC).isoformat(),
        python_version=sys.version,
        platform=platform.platform(),
        parameters_hash=canonical_hash(parameters),
        spectral_source=spectral_source,
        spectral_hash=spectral_hash(gammas),
    )



def serialize_provenance(record: ProvenanceRecord) -> str:
    return json.dumps(asdict(record), indent=2, sort_keys=True)
