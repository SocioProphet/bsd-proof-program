from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path

from m1.campaigns import CampaignResult
from m1.gates import GateResult, GateStatus, all_pass
from m1.provenance import ProvenanceRecord


@dataclass(frozen=True)
class CampaignReport:
    campaign_result: CampaignResult
    gates: list[GateResult]
    provenance: ProvenanceRecord | None
    claim_status: str


class ReportError(RuntimeError):
    pass



def canonical_hash(obj: object) -> str:
    payload = json.dumps(obj, sort_keys=True, default=str)
    return sha256(payload.encode("utf-8")).hexdigest()



def classify_claim_status(gates: list[GateResult]) -> str:
    if not gates:
        return "no_adjudication"
    if any(g.status == GateStatus.INCONCLUSIVE for g in gates):
        return "inconclusive"
    if all_pass(gates):
        return "evidence_passed_no_theorem_claim"
    return "evidence_failed_no_theorem_claim"



def build_campaign_report(
    campaign_result: CampaignResult,
    gates: list[GateResult],
    provenance: ProvenanceRecord | None = None,
) -> CampaignReport:
    return CampaignReport(
        campaign_result=campaign_result,
        gates=gates,
        provenance=provenance,
        claim_status=classify_claim_status(gates),
    )



def write_campaign_report(path: str | Path, report: CampaignReport) -> str:
    payload = asdict(report)
    digest = canonical_hash(payload)
    wrapped = {
        "report_sha256": digest,
        "payload": payload,
    }
    Path(path).write_text(json.dumps(wrapped, indent=2, sort_keys=True, default=str))
    return digest
