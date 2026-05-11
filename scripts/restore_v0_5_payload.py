#!/usr/bin/env python3
"""Restore the packed BSD v0.5 payload into canonical repo paths.

State A infrastructure only. This restores declared data/report files and verifies
SHA-256 identity. It does not promote claims or mark gates as passed.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import shutil
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD_DIR = ROOT / "payloads" / "v0.5"
MANIFEST = PAYLOAD_DIR / "bsd_v05_required_manifest.json"
SINGLE_PAYLOAD = PAYLOAD_DIR / "bsd_v05_required_text.tar.gz.b64"
CHUNK_GLOB = "bsd_v05_required_text.tar.gz.b64.part*"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def read_encoded_payload() -> str:
    if SINGLE_PAYLOAD.exists():
        return "".join(SINGLE_PAYLOAD.read_text(encoding="utf-8").split())
    parts = sorted(PAYLOAD_DIR.glob(CHUNK_GLOB))
    if not parts:
        raise SystemExit(f"no payload file or chunks found under {PAYLOAD_DIR}")
    return "".join("".join(part.read_text(encoding="utf-8").split()) for part in parts)


def decode_payload(expected_sha: str, expected_b64_chars: int | None = None) -> bytes:
    encoded = read_encoded_payload()
    if expected_b64_chars is not None and len(encoded) != expected_b64_chars:
        raise SystemExit(f"payload base64 length mismatch: expected {expected_b64_chars}, got {len(encoded)}")
    payload_bytes = base64.b64decode(encoded)
    actual_sha = sha256_bytes(payload_bytes)
    if actual_sha != expected_sha:
        raise SystemExit(f"payload tar.gz sha mismatch: expected {expected_sha}, got {actual_sha}")
    return payload_bytes


def restore(*, check_only: bool = False) -> None:
    manifest = load_manifest()
    payload_bytes = decode_payload(manifest["payload_tar_gz_sha256"], manifest.get("payload_tar_gz_base64_size_chars"))
    declared = {item["source_path"]: item for item in manifest["files"]}

    with tempfile.TemporaryDirectory(prefix="bsd-v05-payload-") as tmpdir:
        tmp = Path(tmpdir)
        tar_path = tmp / "payload.tar.gz"
        tar_path.write_bytes(payload_bytes)
        unpacked: dict[str, bytes] = {}

        with tarfile.open(tar_path, "r:gz") as tar:
            for member in tar.getmembers():
                if member.isdir():
                    continue
                name = member.name
                if name not in declared:
                    raise SystemExit(f"unexpected payload member: {name}")
                stream = tar.extractfile(member)
                if stream is None:
                    raise SystemExit(f"could not read payload member: {name}")
                unpacked[name] = stream.read()

        restored = []
        for source_name, item in declared.items():
            if source_name not in unpacked:
                raise SystemExit(f"payload source missing: {source_name}")
            data = unpacked[source_name]
            actual_source_sha = sha256_bytes(data)
            if actual_source_sha != item["sha256"]:
                raise SystemExit(f"source sha mismatch for {source_name}: expected {item['sha256']}, got {actual_source_sha}")

            target = ROOT / item["target_path"]
            if not check_only:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)

            if target.exists():
                actual_target_sha = sha256_file(target)
                if actual_target_sha != item["sha256"]:
                    raise SystemExit(f"target sha mismatch for {item['target_path']}: expected {item['sha256']}, got {actual_target_sha}")
            elif check_only:
                raise SystemExit(f"target missing in check mode: {item['target_path']}")
            restored.append(item["target_path"])

    print(f"restore_v0_5_payload: restored_or_checked={len(restored)}")
    for target in restored:
        print(f"  {target}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify already-restored files without writing them.")
    args = parser.parse_args()
    restore(check_only=args.check)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
