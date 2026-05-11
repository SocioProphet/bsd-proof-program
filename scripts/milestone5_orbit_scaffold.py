#!/usr/bin/env python3
"""Milestone 5 orbit-membership scaffold runner.

This runner prepares the first controller-routed M6 surface after Candidate 2.
It verifies inherited P1 points for the four-prime cohort, records target class,
and emits digest-addressed scaffold events.

Boundary: this runner does not search for new points, does not certify
independence, does not run four-descent, and does not promote claims.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "data" / "milestone5" / "m5_four_prime_baseline.json"
OUT = ROOT / "reports" / "milestone5"
TARGETS = {257, 313, 353, 457}


def sha256_json(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def frac(num: int, den: int) -> Fraction:
    return Fraction(num, den)


def on_curve(n: int, point: dict[str, int]) -> bool:
    x = frac(point["x_num"], point["x_den"])
    y = frac(point["y_num"], point["y_den"])
    return y * y == x * x * x - n * n * x


def event(target: dict[str, Any], gate: str, input_payload: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    wrapped_input = {"gate": gate, "n": target["n"], "input": input_payload}
    wrapped_output = {"gate": gate, "n": target["n"], "result": result}
    return {
        "event_type": "milestone5_scaffold_event",
        "gate": gate,
        "n": target["n"],
        "input_digest": "sha256:" + sha256_json(wrapped_input),
        "output_digest": "sha256:" + sha256_json(wrapped_output),
        "result": result,
    }


def main() -> int:
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    targets = baseline.get("targets", [])
    seen = {int(target["n"]) for target in targets}
    if seen != TARGETS:
        raise SystemExit(f"target set mismatch: expected {sorted(TARGETS)}, got {sorted(seen)}")

    events: list[dict[str, Any]] = []
    summary: dict[str, Any] = {
        "state": "Milestone 5 scaffold only",
        "scope_boundary": baseline["claim_boundary"],
        "target_count": len(targets),
        "targets": {},
        "non_claims": [
            "No rank exactness is claimed.",
            "No second independent point is certified.",
            "No four-descent gate has executed.",
            "No BSD-I, BSD-II, or Sha finiteness claim is made."
        ],
    }

    for target in targets:
        n = int(target["n"])
        p1_ok = on_curve(n, target["P1"])
        if not p1_ok:
            raise SystemExit(f"P1 failed on-curve check for n={n}")
        unresolved = target["baseline"].get("second_independent_point_certified") is False
        target_class = target["search_class"]
        result = {
            "p1_on_curve": p1_ok,
            "target_class": target_class,
            "second_independent_point_certified": target["baseline"].get("second_independent_point_certified"),
            "requires_orbit_membership_filter": target_class == "historical_false_positive_requires_orbit_filter",
            "requires_fresh_search_or_descent": target_class == "no_second_generator_found",
            "claim_promotion_allowed": False,
            "unresolved": unresolved,
        }
        events.append(event(target, "m5-p1-on-curve-and-target-classification", {
            "P1": target["P1"],
            "baseline": target["baseline"],
            "search_class": target_class,
            "historical_search": target.get("historical_search"),
        }, result))
        summary["targets"][str(n)] = result

    input_digests = {item["input_digest"] for item in events}
    output_digests = {item["output_digest"] for item in events}
    summary["event_count"] = len(events)
    summary["distinct_input_digest_count"] = len(input_digests)
    summary["distinct_output_digest_count"] = len(output_digests)
    summary["all_p1_on_curve"] = all(item["result"]["p1_on_curve"] for item in events)
    summary["claim_promotion_allowed"] = False

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "m5_scaffold_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with (OUT / "m5_scaffold_events.jsonl").open("w", encoding="utf-8") as handle:
        for item in events:
            handle.write(json.dumps(item, sort_keys=True) + "\n")
    lines = [
        "# Milestone 5 Scaffold Result",
        "",
        "Scope: scaffold only. No rank exactness, independence, four-descent, or claim promotion.",
        "",
        f"- target_count: {summary['target_count']}",
        f"- event_count: {summary['event_count']}",
        f"- distinct_input_digest_count: {summary['distinct_input_digest_count']}",
        f"- distinct_output_digest_count: {summary['distinct_output_digest_count']}",
        f"- all_p1_on_curve: {summary['all_p1_on_curve']}",
        "",
        "## Target classification",
        "",
    ]
    for n in sorted(summary["targets"], key=int):
        lines.append(f"- {n}: {summary['targets'][n]}")
    (OUT / "m5_scaffold_result.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("milestone5_orbit_scaffold: PASS")
    print(f"target_count={summary['target_count']}")
    print(f"event_count={summary['event_count']}")
    print(f"distinct_input_digest_count={summary['distinct_input_digest_count']}")
    print(f"distinct_output_digest_count={summary['distinct_output_digest_count']}")
    print(f"all_p1_on_curve={summary['all_p1_on_curve']}")
    print(f"targets={json.dumps(summary['targets'], sort_keys=True)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
