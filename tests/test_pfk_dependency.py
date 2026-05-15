from pathlib import Path
import os
import unittest


ROOT = Path(__file__).resolve().parents[1]
PIN = "988307215ad38ccb16514311222184a1b757752b"
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
    def test_dependencies_file_exists_and_pins_commit(self) -> None:
        path = ROOT / "DEPENDENCIES.md"
        self.assertTrue(path.exists())
        text = path.read_text(encoding="utf-8")
        self.assertIn(PIN, text)
        self.assertIn("HG-MTH-005", text)
        self.assertIn("PFK-SCHEMA-001", text)
        self.assertIn("A-PFK-OP-001", text)

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
