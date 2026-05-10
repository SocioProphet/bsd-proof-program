# M6.0 First Action Runbook

Purpose: freeze the inherited baseline and produce the manifest artifacts that every later M6 stage consumes. This runbook performs no descent, no point search, no promotion, and no row-state changes.

## Preconditions

Run from repository root on a clean checkout.

Required files:

```text
data/v0.3.1/bsd_dataset_v0_3_1.json
data/v0.3.1/bsd_dataset_v0_3_1.csv
reports/v0.3.1/bsd_dataset_v0_3_1_validation.json
```

M6 target rows:

```text
{257, 313, 353, 457}
```

## Naming note

The M6 schema keeps the slot name `v0_5_inherited` for contract continuity. In v0.3.2, that slot may be populated from the v0.3.1-normalized baseline. The field name is historical; the manifest must record the actual source filenames and hashes.

## Step 1 — Verify inherited inputs exist

```bash
python3 - <<'PY'
from pathlib import Path
required = [
    Path('data/v0.3.1/bsd_dataset_v0_3_1.json'),
    Path('data/v0.3.1/bsd_dataset_v0_3_1.csv'),
    Path('reports/v0.3.1/bsd_dataset_v0_3_1_validation.json'),
]
missing = [str(p) for p in required if not p.exists()]
if missing:
    raise SystemExit('Missing required inherited input(s):\n' + '\n'.join(missing))
print('M6.0 input files present')
PY
```

## Step 2 — Compute file SHA-256 manifest

```bash
mkdir -p reports/v0.6/m6.0
python3 - <<'PY'
import hashlib
from pathlib import Path
files = [
    Path('data/v0.3.1/bsd_dataset_v0_3_1.csv'),
    Path('data/v0.3.1/bsd_dataset_v0_3_1.json'),
    Path('reports/v0.3.1/bsd_dataset_v0_3_1_validation.json'),
]
lines = []
for p in sorted(files, key=lambda x: str(x)):
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    lines.append(f'{h}  {p.as_posix()}')
out = Path('reports/v0.6/m6.0/MANIFEST_v0_5.sha256')
out.write_text('\n'.join(lines) + '\n')
print(out.read_text())
PY
```

`MANIFEST_v0_5.sha256` preserves the historical M6 slot name. Its content must identify v0.3.1 files explicitly.

## Step 3 — Verify baseline row counts

```bash
python3 - <<'PY'
import json
from collections import Counter
from pathlib import Path
rows = json.loads(Path('data/v0.3.1/bsd_dataset_v0_3_1.json').read_text())
assert len(rows) == 608, len(rows)
counts = Counter(r.get('evidence_class') for r in rows)
assert counts['E1'] == 307, counts
assert counts['E2'] == 301, counts
for n in {257, 313, 353, 457}:
    row = next((r for r in rows if r.get('n') == n), None)
    assert row is not None, f'target {n} missing'
    assert row.get('evidence_class') == 'E1', f'target {n} not E1: {row.get("evidence_class")}'
print('v0.3.1 baseline count check passed: 608 rows, E1=307, E2=301')
PY
```

## Step 4 — Compute audit-correction hash

The validation report must carry an `audit_correction` block. It must include the M5.1 second-generator false positives at p=313 and p=353. Hash canonical JSON of that block.

```bash
python3 - <<'PY'
import hashlib
import json
from pathlib import Path
validation = json.loads(Path('reports/v0.3.1/bsd_dataset_v0_3_1_validation.json').read_text())
if 'audit_correction' not in validation:
    raise SystemExit('Missing audit_correction block in v0.3.1 validation report')
block = validation['audit_correction']
false_positives = set(block.get('false_positives_caught', []))
for n in (313, 353):
    if n not in false_positives:
        raise SystemExit(f'Missing carried-forward false positive p={n}')
canonical = json.dumps(block, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
h = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
Path('reports/v0.6/m6.0/audit_correction.sha256').write_text(h + '\n')
print(h)
PY
```

This hash becomes `v0_5_inherited.audit_correction_hash` in every M6 row certificate.

## Step 5 — Write ingest report and claim manifest

```bash
python3 - <<'PY'
import hashlib
import json
from collections import Counter
from pathlib import Path
rows = json.loads(Path('data/v0.3.1/bsd_dataset_v0_3_1.json').read_text())
validation_path = Path('reports/v0.3.1/bsd_dataset_v0_3_1_validation.json')
validation = json.loads(validation_path.read_text())
manifest_path = Path('reports/v0.6/m6.0/MANIFEST_v0_5.sha256')
audit_hash_path = Path('reports/v0.6/m6.0/audit_correction.sha256')
counts = Counter(r.get('evidence_class') for r in rows)
report = {
    'stage': 'M6.0',
    'source_dataset_version': 'v0.3.1-normalized',
    'schema_slot': 'v0_5_inherited',
    'total_rows': len(rows),
    'evidence_class_counts': dict(counts),
    'target_rows': [257, 313, 353, 457],
    'manifest_file': manifest_path.as_posix(),
    'audit_correction_hash': audit_hash_path.read_text().strip(),
    'validation_report_sha256': hashlib.sha256(validation_path.read_bytes()).hexdigest(),
    'no_promotions': True,
}
Path('reports/v0.6/m6.0/v0_5_ingest_report.json').write_text(json.dumps(report, indent=2) + '\n')
claim = f'''# M6.0 Claim Manifest\n\n- Stage: M6.0\n- Source dataset: v0.3.1-normalized\n- Schema slot: v0_5_inherited\n- Rows: {len(rows)}\n- E1: {counts.get('E1', 0)}\n- E2: {counts.get('E2', 0)}\n- Target rows: {{257, 313, 353, 457}}\n- Promotions made: none\n- Mathematical claims made: none\n- Audit correction hash: {report['audit_correction_hash']}\n'''
Path('reports/v0.6/m6.0/v0_5_claim_manifest.md').write_text(claim)
print('M6.0 ingest artifacts written')
PY
```

## Step 6 — Abort if later M6 artifacts already exist

Before running M6.0 on a real branch, no later-stage M6 outputs may exist.

```bash
python3 - <<'PY'
from pathlib import Path
bad = []
if Path('data/v0.6').exists():
    bad.append('data/v0.6')
root = Path('reports/v0.6')
if root.exists():
    bad.extend(str(p) for p in root.glob('m6.[1-8]*'))
if bad:
    raise SystemExit('Refusing M6.0: later-stage outputs already exist:\n' + '\n'.join(bad))
print('No later-stage M6 outputs found')
PY
```

## Step 7 — Stop

Do not run M6.1 in the same script unless M6.0 outputs have been reviewed and committed.
