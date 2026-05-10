# Local Binary-Capable Sync Commands

These commands complete the full byte-for-byte archive expansion into the authoritative repo when run on a machine with GitHub push access and the uploaded archive available locally.

The GitHub connector used for the current session can update UTF-8 files and metadata but cannot directly push local binary/PDF/archive bytes from `/mnt/data` into GitHub as native repository files. Use this runbook to complete the path-preserving import.

## Preconditions

- GitHub push access to `SocioProphet/bsd-proof-program`.
- Local copy of `bsd-m6-scaffolding-v0.3.2.zip`.
- Python 3.10+.
- Optional: `pdftotext` / `poppler-utils` if running the full CI-equivalent PDF readability checks.

Expected archive hash:

```text
41990051925e4b04e22e0b50f7be01cd8a6c5b87894ee354a1bc696112a5ad1e  bsd-m6-scaffolding-v0.3.2.zip
```

## Full import commands

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
  git clone git@github.com:SocioProphet/bsd-proof-program.git "$WORKDIR"
fi
cd "$WORKDIR"
git fetch origin

# 4. Create import branch from current main.
git checkout main
git pull --ff-only origin main
git checkout -B m6-scaffolding-v0.3.2-full-import

# 5. Replace repo contents with flattened archive contents.
#    Keep .git only.
find . -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
rm -rf "$IMPORTDIR"
mkdir -p "$IMPORTDIR"
unzip -q "$BSD_ZIP" -d "$IMPORTDIR"
rsync -a "$IMPORTDIR/bsd-m6-scaffolding-v0.3.2/" ./

# 6. Verify expected file count before generated outputs.
find . -type f ! -path './.git/*' | sort > /tmp/bsd-m6-import-file-list.txt
wc -l /tmp/bsd-m6-import-file-list.txt
# Expected baseline: 36 files.

# 7. Run pre-flight validation.
python3 scripts/smoke_test.py
python3 -m py_compile \
  m6/models/m6_v0_6_models.py \
  m6/scripts/m6_0_freeze_v0_5.py \
  scripts/smoke_test.py \
  tests/test_m6_targets.py

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt pytest pydantic
pytest -q tests/test_m6_targets.py

# 8. Run M6.0 freeze as validation, then remove generated v0.6 outputs
#    from this baseline commit unless explicitly creating a post-freeze commit.
python3 -m m6.scripts.m6_0_freeze_v0_5
ls -la reports/v0.6/m6.0
rm -rf reports/v0.6

# 9. Confirm generated outputs are not accidentally included.
git status --short

# 10. Commit and push.
git add .
git commit -m "Import BSD M6 scaffolding v0.3.2 baseline"
git push -u origin m6-scaffolding-v0.3.2-full-import
```

## PR body template

```markdown
## Summary

Imports `bsd-m6-scaffolding-v0.3.2.zip` as the authoritative M6 pre-execution scaffolding baseline for `SocioProphet/bsd-proof-program`.

Source archive:

```text
sha256: 41990051925e4b04e22e0b50f7be01cd8a6c5b87894ee354a1bc696112a5ad1e
```

## Validation

- `python3 scripts/smoke_test.py`
- `python3 -m py_compile ...`
- `pytest -q tests/test_m6_targets.py`
- `python3 -m m6.scripts.m6_0_freeze_v0_5`

## Claim boundary

Baseline capture only. No descent computation. No dataset promotion. No new mathematical claim.

Closes #1.
```

## Important boundary

Do not start M6.1 until the full import PR is merged and validation is observed on GitHub Actions or equivalent local output is attached to #1.
