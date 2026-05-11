#!/usr/bin/env python3
"""Restore the packed BSD v0.5 payload into canonical repo paths.

The payload is stored as a base64-encoded gzip tarball so text/data assets from
an uploaded archive can be preserved through connector paths that cannot attach
native binary files directly.

This script is State A infrastructure only. It restores data/scripts/docs and
verifies SHA-256 identity; it does not promote claims or mark gates as passed.
"""

from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
import shutil
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "payloads" / "v0.5" / "bsd_v05_required_manifest.json"
PAYLOAD = ROOT / "payloads" / "v0.5" / "bsd_v05_required_text.tar.gz.b64"


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


def decode_payload(expected_sha: str) -> bytes:
    encoded = "".join(PAYLOAD.read_text(encoding="utf-8").split())
    payload_bytes = base64.b64decode(encoded)
    actual_sha = sha256_bytes(payload_bytes)
    if actual_sha != expected_sha:
        raise SystemExit(f"payload tar.gz sha mismatch: expected {expected_sha}, got {actual_sha}")
    return payload_bytes


def restore(*, check_only: bool = False) -> None:
    manifest = load_manifest()
    payload_bytes = decode_payload(manifest["payload_tar_gz_sha256"])

    with tempfile.TemporaryDirectory(prefix="bsd-v05-payload-") as tmpdir:
        tmp = Path(tmpdir)
        tar_path = tmp / "payload.tar.gz"
        tar_path.write_bytes(payload_bytes)

        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall(tmp / "src")

        restored = []
        for item in manifest["files"]:
            source = tmp / "src" / item["source_path"]
            target = ROOT / item["target_path"]
            if not source.exists():
                raise SystemExit(f"payload source missing: {item['source_path']}")
            data = source.read_bytes()
            actual_source_sha = sha256_bytes(data)
            if actual_source_sha != item["sha256"]:
                raise SystemExit(
                    f"source sha mismatch for {item['source_path']}: "
                    f"expected {item['sha256']}, got {actual_source_sha}"
                )
            if not check_only:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
            if target.exists():
                actual_target_sha = sha256_file(target)
                if actual_target_sha != item["sha256"]:
                    raise SystemExit(
                        f"target sha mismatch for {item['target_path']}: "
                        f"expected {item['sha256']}, got {actual_target_sha}"
                    )
            elif check_only:
                raise SystemExit(f"target missing in check mode: {item['target_path']}")
            restored.append(item["target_path"])

    print(f"restore_v0_5_payload: restored_or_checked={len(restored)}")
    for target in restored:
        print(f"  {target}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify already-restored files without writing them.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    restore(check_only=args.check)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
