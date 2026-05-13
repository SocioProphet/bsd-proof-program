from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from m1.campaigns import CampaignResult
from m1.gates import GateResult, GateStatus, perturbation_robustness_gate, shuffled_collapse_gate
from m1.provenance import ProvenanceRecord
from m1.serialization import to_jsonable


@dataclass(frozen=True)
class PairComparisonReport:
    comparison_kind: str
    summary_key: str
    canonical_result: CampaignResult
    control_result: CampaignResult
    canonical_energy: float
    control_energy: float
    gate: GateResult
    provenance: ProvenanceRecord | None
    claim_status: str


class ComparisonError(RuntimeError):
    pass


def _summary_energy(result: CampaignResult, summary_key: str) -> float:
    try:
        return result.sweep_result.summaries[summary_key].energy
    except KeyError as exc:
        raise ComparisonError(f"missing summary key: {summary_key}") from exc


def _claim_status(gate: GateResult) -> str:
    if gate.status == GateStatus.INCONCLUSIVE:
        return "inconclusive"
    if gate.status == GateStatus.PASS:
        return "evidence_passed_no_theorem_claim"
    return "evidence_failed_no_theorem_claim"


def compare_shuffled_collapse(
    canonical_result: CampaignResult,
    shuffled_result: CampaignResult,
    summary_key: str,
    min_ratio: float,
    provenance: ProvenanceRecord | None = None,
) -> PairComparisonReport:
    canonical_energy = _summary_energy(canonical_result, summary_key)
    shuffled_energy = _summary_energy(shuffled_result, summary_key)
    gate = shuffled_collapse_gate(canonical_energy, shuffled_energy, min_ratio)
    return PairComparisonReport(
        comparison_kind="shuffled_collapse",
        summary_key=summary_key,
        canonical_result=canonical_result,
        control_result=shuffled_result,
        canonical_energy=canonical_energy,
        control_energy=shuffled_energy,
        gate=gate,
        provenance=provenance,
        claim_status=_claim_status(gate),
    )


def compare_perturbation_robustness(
    canonical_result: CampaignResult,
    perturbed_result: CampaignResult,
    summary_key: str,
    max_relative_delta: float,
    provenance: ProvenanceRecord | None = None,
) -> PairComparisonReport:
    canonical_energy = _summary_energy(canonical_result, summary_key)
    perturbed_energy = _summary_energy(perturbed_result, summary_key)
    gate = perturbation_robustness_gate(
        canonical_energy,
        perturbed_energy,
        max_relative_delta,
    )
    return PairComparisonReport(
        comparison_kind="perturbation_robustness",
        summary_key=summary_key,
        canonical_result=canonical_result,
        control_result=perturbed_result,
        canonical_energy=canonical_energy,
        control_energy=perturbed_energy,
        gate=gate,
        provenance=provenance,
        claim_status=_claim_status(gate),
    )


def canonical_hash(obj: object) -> str:
    payload = json.dumps(to_jsonable(obj), sort_keys=True)
    return sha256(payload.encode("utf-8")).hexdigest()


def write_pair_report(path: str | Path, report: PairComparisonReport) -> str:
    payload = to_jsonable(report)
    digest = canonical_hash(payload)
    wrapped = {
        "pair_report_sha256": digest,
        "payload": payload,
    }
    Path(path).write_text(json.dumps(wrapped, indent=2, sort_keys=True))
    return digest
