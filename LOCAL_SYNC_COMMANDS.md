# Local Binary-Capable State A Import Commands

These commands complete the full byte-for-byte archive expansion into the authoritative repo when run on a machine with GitHub push access and the uploaded archive available locally.

The current connector path can update UTF-8 files and metadata, but it cannot honestly complete the binary/PDF/archive-preserving import without the source archive being available to this session. Use this runbook to land the State A import tracked by #7.

## Import state

This import must land as **State A — infrastructure import only** unless a separate PR explicitly supplies controller-witnessed gate evidence.

State A means:

- import data, scripts, tests, reports, specs, and docs;
- do not claim new M6 execution;
- keep `BSD-M6-002-four-descent-named-primes` at `draft` / `E7`;
- do not set any gate to `pass` unless controller-witnessed input/output SHA-256 digests are supplied;
- do not promote any claim;
- keep Candidate 2 as a separate positive-path replay after import.

## Preconditions

- GitHub push access to `SocioProphet/bsd-proof-program`.
- Local copy of `bsd-m6-scaffolding-v0.3.2.zip`.
- Python 3.10+.
- Optional: `pdftotext` / `poppler-utils` if running PDF readability checks.

Expected archive hash:

```text
41990051925e4b04e22e0b50f7be01cd8a6c5b87894ee354a1bc696112a5ad1e  bsd-m6-scaffolding-v0.3.2.zip
```

## Full State A import commands

```bash
set -euo pipefail

# 1. Choose working paths.
export BSD_ZIP="/absolute/path/to/bsd-m6-scaffolding-v0.3.2.zip"
export WORKDIR="$HOME/dev/bsd-proof-program"
export IMPORTDIR="/tmp/bsd-m6-import"

# 2. Verify source archive before touching repo state.
sha256sum "$BSD_ZIP"
test "$(sha256sum "$BSD_ZIP" | awk '{print $1}')" = "41990051925e4b04e22e0b50f7be01cd8a6c5b87894ee354a1bc696112a5ad1e"

# 3. Clone or refresh authoritative repo.
mkdir -p "$HOME/dev"
if [ ! -d "$WORKDIR/.git" ]; then
  gh repo clone SocioProphet/bsd-proof-program "$WORKDIR"
fi
cd "$WORKDIR"
git fetch origin

# 4. Create import branch from current main.
git checkout main
git pull --ff-only origin main
git checkout -B state-a/v0.3.2-v0.5-full-import

# 5. Replace repo contents with flattened archive contents.
#    Keep .git only.
find . -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
rm -rf "$IMPORTDIR"
mkdir -p "$IMPORTDIR"
unzip -q "$BSD_ZIP" -d "$IMPORTDIR"
rsync -a "$IMPORTDIR/bsd-m6-scaffolding-v0.3.2/" ./

# 6. Reapply the current proof-adapter and continuous-validation workflow if the
#    archive predates SocioSphere proof apparatus wiring.
git checkout origin/main -- proof-adapter.json .github/workflows/proof-apparatus-continuous-validation.yml || true

# 7. Verify expected files are present.
test -f data/v0.5/bsd_dataset_v0_5.csv
test -f data/v0.5/bsd_dataset_v0_5.json
test -f reports/v0.5/bsd_dataset_v0_5_validation.json
test -f m6/models/m6_v0_6_models.py
test -f m6/scripts/m6_0_freeze_v0_5.py
test -f scripts/smoke_test.py
test -f tests/test_m6_targets.py

# 8. Run pre-flight validation.
python3 scripts/smoke_test.py
python3 -m py_compile \
  m6/models/m6_v0_6_models.py \
  m6/scripts/m6_0_freeze_v0_5.py \
  scripts/smoke_test.py \
  tests/test_m6_targets.py

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt pytest pydantic
pytest -q tests/test_m6_targets.py

# 9. Run M6.0 freeze as validation, then remove generated v0.6 outputs
#    from this State A baseline commit unless explicitly creating a later
#    post-freeze evidence PR.
python3 -m m6.scripts.m6_0_freeze_v0_5
ls -la reports/v0.6/m6.0
rm -rf reports/v0.6

# 10. Confirm the adapter remains State A.
python3 - <<'PY'
import json
adapter = json.load(open('proof-adapter.json'))
claims = {c['claim_id']: c for c in adapter.get('claims', [])}
m6 = claims['BSD-M6-002-four-descent-named-primes']
assert m6['state'] == 'draft', m6
assert m6['severity'] == 'E7', m6
for gate in adapter.get('gates', []):
    assert gate.get('status') != 'pass', gate
print('State A adapter posture verified: BSD-M6-002 remains draft/E7; no passed gates.')
PY

# 11. Commit and push.
git status --short
git add .
git commit -m "State A import BSD M6 scaffolding v0.3.2 baseline"
git push -u origin state-a/v0.3.2-v0.5-full-import
```

## PR body template

```markdown
## Summary

State A infrastructure import for `bsd-m6-scaffolding-v0.3.2.zip` into `SocioProphet/bsd-proof-program`.

This PR imports the v0.5/v0.3.2 baseline data, scripts, tests, reports, specs, and docs required before Candidate 2 C5 replay.

Source archive:

```text
sha256: 41990051925e4b04e22e0b50f7be01cd8a6c5b87894ee354a1bc696112a5ad1e
```

## Import state

State A — infrastructure import only.

No new M6 execution is claimed. `BSD-M6-002-four-descent-named-primes` remains `draft` / `E7`. No gate is marked `pass`. No claim is promoted.

## Validation

- `python3 scripts/smoke_test.py`
- `python3 -m py_compile ...`
- `pytest -q tests/test_m6_targets.py`
- `python3 -m m6.scripts.m6_0_freeze_v0_5`
- State A adapter-posture check: `BSD-M6-002-four-descent-named-primes == draft/E7`

## Candidate 2

This import unblocks Candidate 2 only after CI confirms the imported files are present and loadable. Candidate 2 remains a separate positive-path SocioSphere proof-apparatus replay.

Closes #7.
```

## Important boundary

Do not start Candidate 2, M6.1, or Milestone 5 until the State A import PR is merged and validation is observed on GitHub Actions or equivalent local output is attached to #7.
