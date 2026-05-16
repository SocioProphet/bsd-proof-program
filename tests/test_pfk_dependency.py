from pathlib import Path
import os
import unittest


ROOT = Path(__file__).resolve().parents[1]
HELLER_GODEL_COMMIT = "e385bad859c49604cff5a3f4945b33079d54af82"
HELLER_DIRAC_COMMIT = "e1d7c863f4e0fc6e5e2ab485370cc75b2dba3993"
REQUIRED_PFK_PATHS = [
    "proof_fabric_kernel/docs/OperatorCatalog_PrimePolicyOperators_v1.md",
    "proof_fabric_kernel/docs/SchemaCatalog_v1.md",
    "proof_fabric_kernel/docs/anti-seed-pfk.md",
    "proof_fabric_kernel/schemas/claim_ledger_row.schema.json",
    "proof_fabric_kernel/schemas/event_ir.schema.json",
    "proof_fabric_kernel/schemas/proof_artifact.schema.json",
    "proof_fabric_kernel/schemas/calibration_bundle.schema.json",
]
CANONICAL_SCHEMA_NAMES = {
    "claim_ledger_row.schema.json",
    "event_ir.schema.json",
    "proof_artifact.schema.json",
    "calibration_bundle.schema.json",
}


class TestPFKDependency(unittest.TestCase):
    def test_dependencies_file_exists_and_pins_both_upstreams(self) -> None:
        path = ROOT / "DEPENDENCIES.md"
        self.assertTrue(path.exists())
        text = path.read_text(encoding="utf-8")
        self.assertIn(HELLER_GODEL_COMMIT, text)
        self.assertIn(HELLER_DIRAC_COMMIT, text)
        self.assertIn("HG-MTH-009", text)
        self.assertIn("A-HG-MTH-007", text)
        self.assertIn("HD-FND-001", text)
        self.assertIn("HD-FND-007", text)
        self.assertIn("HD-EX-001", text)
        self.assertIn("A-HD-NC-001", text)
        self.assertIn("PFK-SCHEMA-001", text)
        self.assertIn("A-PFK-OP-001", text)

    def test_bsd_bridge_citation_anchor_exists(self) -> None:
        path = ROOT / "docs" / "scope" / "bsd-bridge-citation.md"
        self.assertTrue(path.exists())
        text = path.read_text(encoding="utf-8")
        self.assertIn("HG-MTH-009", text)
        self.assertIn("A-HG-MTH-007", text)
        self.assertIn(HELLER_GODEL_COMMIT, text)
        self.assertIn(HELLER_DIRAC_COMMIT, text)

    def test_no_local_canonical_schema_shadowing(self) -> None:
        local_schemas = ROOT / "schemas"
        if not local_schemas.exists():
            return
        local_names = {path.name for path in local_schemas.rglob("*.json")}
        shadowed = sorted(local_names & CANONICAL_SCHEMA_NAMES)
        self.assertFalse(shadowed, f"local schemas shadow canonical PFK schemas: {shadowed}")

    def test_canonical_pfk_schemas_resolve_when_available(self) -> None:
        hg_root_value = os.environ.get("HELLER_GODEL_ROOT")
        if not hg_root_value:
            self.skipTest("HELLER_GODEL_ROOT not set; dependency-resolution check runs in dedicated workflow")
        hg_root = Path(hg_root_value)
        missing = [path for path in REQUIRED_PFK_PATHS if not (hg_root / path).exists()]
        self.assertFalse(missing, f"Missing canonical Heller-Godel PFK paths: {missing}")
        spec = hg_root / "docs" / "framework-core" / "universal-bridge" / "HG-MTH-009-bsd-bridge-spec.md"
        self.assertTrue(spec.exists(), f"HG-MTH-009 spec missing at {HELLER_GODEL_COMMIT}")

    def test_heller_dirac_paths_resolve_when_available(self) -> None:
        hd_root_value = os.environ.get("HELLER_DIRAC_ROOT")
        if not hd_root_value:
            self.skipTest("HELLER_DIRAC_ROOT not set; dependency-resolution check runs in dedicated workflow")
        hd_root = Path(hd_root_value)
        foundations = hd_root / "docs" / "foundations"
        for ident in ["HD-FND-001", "HD-FND-007"]:
            matches = list(foundations.glob(f"{ident}-*.md"))
            self.assertTrue(matches, f"Missing {ident} at Heller-Dirac pin {HELLER_DIRAC_COMMIT}")
        fixture = hd_root / "docs" / "fixtures" / "HD-EX-001-circle-spectral-triple.md"
        self.assertTrue(fixture.exists(), f"Missing HD-EX-001 at Heller-Dirac pin {HELLER_DIRAC_COMMIT}")

    def test_workstream_skeletons_exist(self) -> None:
        expected = {f"workstream-{letter}" for letter in "abcdef"}
        docs = ROOT / "docs"
        found = {d.name for d in docs.iterdir() if d.is_dir() and d.name.startswith("workstream-")}
        self.assertTrue(expected.issubset(found), f"Missing workstream skeletons: {expected - found}")

    def test_program_spec_skeleton_exists(self) -> None:
        spec_path = ROOT / "docs" / "program-spec" / "bsd-program-lane-v0_1.md"
        self.assertTrue(spec_path.exists())
        content = spec_path.read_text(encoding="utf-8")
        for letter in "ABCDEF":
            self.assertIn(f"Workstream {letter}", content)
        self.assertIn("full PDF text not imported", content)


if __name__ == "__main__":
    unittest.main()
