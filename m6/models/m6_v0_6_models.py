"""Pydantic contract for BSD M6 v0.6 row certificates.

This model is a pre-execution type contract. It does not compute descent,
rank, Sha, or point independence. It validates that any emitted M6 row is
internally coherent, hash-addressed, and honest about inconclusive or failed
engine states.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


EngineRole = Literal[
    "four_descent",
    "point_search",
    "independence_check",
    "curve_verification",
    "audit",
]
EngineStatus = Literal["success", "inconclusive", "error", "invalidated"]
PointSource = Literal[
    "bounded_search",
    "heegner",
    "four_descent",
    "imported_certificate",
    "manual_review",
]
IndependenceStatus = Literal[
    "independent",
    "dependent",
    "not_checked",
    "not_applicable",
]
Outcome = Literal[
    "rank_exact_1",
    "rank_exact_2",
    "rank_still_1_or_2",
    "engine_inconclusive",
    "engine_error",
    "certificate_invalid",
]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class SearchBounds(StrictModel):
    """Declared search/descent bounds for an attempted engine run."""

    method: str
    D_max: int | None = None
    c_abs_max: int | None = None
    height_bound: str | None = None
    prime_bound: int | None = None
    time_limit_s: float | None = None
    notes: str | None = None


class EngineRun(StrictModel):
    """Auditable execution record for an M6 engine or verifier."""

    engine_id: str
    engine_name: str
    engine_version: str
    role: EngineRole
    status: EngineStatus
    started_at: str | None = None
    completed_at: str | None = None
    input_hash: str | None = None
    output_hash: str | None = None
    log_hash: str | None = None
    notes: str | None = None


class PointCertificate(StrictModel):
    """Certificate for a rational point on E_n."""

    x: str
    y: str
    source: PointSource
    on_curve_verified: bool
    torsion_excluded: bool
    independence_status: IndependenceStatus = "not_checked"
    verification_notes: str | None = None

    @model_validator(mode="after")
    def _promotion_ready_points_are_real(self) -> "PointCertificate":
        if self.independence_status == "independent":
            if not self.on_curve_verified or not self.torsion_excluded:
                raise ValueError(
                    "independent point claims require on-curve verification and torsion exclusion"
                )
        return self


class FourDescentBlock(StrictModel):
    """Four-descent evidence block.

    The key invariant is that attempted four-descent must have auditable engine
    runs, declared search bounds, and a unique primary four-descent run.
    """

    attempted: bool = False
    search_bounds: SearchBounds | None = None
    primary_engine: str | None = None
    engine_runs: list[EngineRun] = Field(default_factory=list)
    certificate_status: Literal[
        "not_attempted",
        "success",
        "inconclusive",
        "error",
        "invalid",
    ] = "not_attempted"
    descent_rank_upper_bound: int | None = None
    sha2_dimension_exact: int | None = None
    notes: str | None = None

    @model_validator(mode="after")
    def _attempted_requires_engine_audit(self) -> "FourDescentBlock":
        if not self.attempted:
            if self.certificate_status != "not_attempted":
                raise ValueError("unattempted four-descent must use certificate_status='not_attempted'")
            return self

        if self.search_bounds is None:
            raise ValueError("four_descent.attempted requires search_bounds")
        if not self.engine_runs:
            raise ValueError("four_descent.attempted requires at least one engine run")
        if self.primary_engine is None:
            raise ValueError("four_descent.attempted requires primary_engine")

        primary_matches = [
            run
            for run in self.engine_runs
            if run.role == "four_descent" and run.engine_id == self.primary_engine
        ]
        if len(primary_matches) != 1:
            raise ValueError(
                "primary_engine must equal exactly one engine_runs entry with role='four_descent'"
            )
        return self


class V05InheritedBlock(StrictModel):
    """Inherited baseline metadata.

    The field name is retained for M6 contract continuity. The underlying
    source may be the v0.3.1-normalized baseline, but the slot remains the
    M6 inheritance block.
    """

    source_dataset_version: str = "v0.3.1-normalized"
    source_dataset_json_sha256: str
    source_dataset_csv_sha256: str | None = None
    source_validation_sha256: str | None = None
    audit_correction_hash: str
    inherited_evidence_class: str
    inherited_claim_tier: str
    inherited_notes: str | None = None


class M6RowCertificate(StrictModel):
    """Top-level M6 v0.6 row certificate."""

    schema_version: Literal["m6.v0.6"] = "m6.v0.6"
    n: int
    curve: str
    row_id: str
    v0_5_inherited: V05InheritedBlock
    e2_rational_dimension: Literal[2] = 2
    points_discovered: list[PointCertificate] = Field(default_factory=list)
    four_descent: FourDescentBlock = Field(default_factory=FourDescentBlock)
    outcome: Outcome
    alg_rank_exact_known: bool
    alg_rank_exact: int | None = None
    rank_lower_bound: int | None = None
    rank_upper_bound: int | None = None
    sha2_dimension_exact: int | None = None
    promotion_notes: str | None = None
    row_hash: str = ""

    @staticmethod
    def canonical_hash(payload: dict[str, Any]) -> str:
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return hashlib.sha256(encoded.encode("utf-8")).hexdigest()

    def payload_without_hash(self) -> dict[str, Any]:
        return self.model_dump(mode="json", exclude={"row_hash"})

    @classmethod
    def with_computed_hash(cls, **kwargs: Any) -> "M6RowCertificate":
        provisional = cls(**{**kwargs, "row_hash": "PENDING"})
        payload = provisional.payload_without_hash()
        return cls(**{**kwargs, "row_hash": cls.canonical_hash(payload)})

    @model_validator(mode="after")
    def _semantic_consistency(self) -> "M6RowCertificate":
        if self.n <= 0:
            raise ValueError("n must be positive")
        if self.e2_rational_dimension != 2:
            raise ValueError("congruent-number family requires e2_rational_dimension=2")

        failed_outcomes = {"engine_inconclusive", "engine_error", "certificate_invalid"}
        if self.outcome in failed_outcomes:
            if self.alg_rank_exact_known or self.alg_rank_exact is not None:
                raise ValueError(
                    "inconclusive/error/invalid outcomes must not carry exact algebraic rank"
                )

        if self.outcome == "rank_still_1_or_2" and not self.four_descent.attempted:
            raise ValueError("rank_still_1_or_2 requires an attempted four-descent block")

        if self.outcome == "rank_exact_1":
            if not self.alg_rank_exact_known or self.alg_rank_exact != 1:
                raise ValueError("rank_exact_1 requires alg_rank_exact_known=True and alg_rank_exact=1")
            if not self.four_descent.attempted:
                raise ValueError("rank_exact_1 requires attempted descent to close the upper bound")
            if not any(p.on_curve_verified and p.torsion_excluded for p in self.points_discovered):
                raise ValueError("rank_exact_1 requires at least one verified non-torsion point")

        if self.outcome == "rank_exact_2":
            if not self.alg_rank_exact_known or self.alg_rank_exact != 2:
                raise ValueError("rank_exact_2 requires alg_rank_exact_known=True and alg_rank_exact=2")
            independent_points = [
                p
                for p in self.points_discovered
                if p.on_curve_verified
                and p.torsion_excluded
                and p.independence_status == "independent"
            ]
            if len(independent_points) < 2:
                raise ValueError("rank_exact_2 requires at least two verified independent non-torsion points")

        expected_hash = self.canonical_hash(self.payload_without_hash())
        if self.row_hash in {"", "PENDING", "__compute__"}:
            self.row_hash = expected_hash
        elif self.row_hash != expected_hash:
            raise ValueError(f"row_hash mismatch: expected {expected_hash}, got {self.row_hash}")
        return self


def validate_row_dict(row: dict[str, Any]) -> M6RowCertificate:
    """Validate a raw row dict and return the normalized certificate."""

    return M6RowCertificate(**row)
