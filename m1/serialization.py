from __future__ import annotations

from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any



def to_jsonable(obj: Any) -> Any:
    """Convert dataclass/Enum-rich M1 objects into stable JSON values."""
    if isinstance(obj, Enum):
        return obj.value

    if is_dataclass(obj):
        return to_jsonable(asdict(obj))

    if isinstance(obj, dict):
        return {str(k): to_jsonable(v) for k, v in obj.items()}

    if isinstance(obj, (list, tuple)):
        return [to_jsonable(v) for v in obj]

    return obj
