from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from m1.benchmarks import BenchmarkInterval, get_interval
from m1.campaigns import CampaignKind, CampaignResult, CampaignSpec, SpectralControl
from m1.experiments import SweepSpec
from m1.gates import (
    GateResult,
    autocorrelation_gate,
    perturbation_robustness_gate,
    shuffled_collapse_gate,
    stationarity_gate,
)
from m1.normalization import NormalizationMode
from m1.perturbation import PerturbationSpec


@dataclass(frozen=True)
class GateSpec:
    name: str
    params: dict[str, Any]


@dataclass(frozen=True)
class CampaignEnvelope:
    campaign: CampaignSpec
    gates: list[GateSpec]
    spectral_source: str


class CampaignIOError(RuntimeError):
    pass



def load_gammas(path: str | Path) -> list[float]:
    vals: list[float] = []
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        vals.append(float(line.split()[0]))
    if not vals:
        raise CampaignIOError("gamma file did not contain any usable values")
    return vals



def _interval_from_dict(obj: dict[str, Any]) -> BenchmarkInterval:
    if "ref" in obj:
        return get_interval(str(obj["ref"]))
    return BenchmarkInterval(
        name=str(obj["name"]),
        left=int(obj["left"]),
        right=int(obj["right"]),
        du=float(obj["du"]),
    )



def parse_campaign_envelope(obj: dict[str, Any]) -> CampaignEnvelope:
    try:
        sweep_obj = obj["sweep"]
        campaign_obj = obj["campaign"]
    except KeyError as exc:
        raise CampaignIOError(f"missing required campaign field: {exc}") from exc

    sweep = SweepSpec(
        name=str(sweep_obj["name"]),
        intervals=[_interval_from_dict(x) for x in sweep_obj["intervals"]],
        truncation_levels=[int(x) for x in sweep_obj["truncation_levels"]],
        du_values=[float(x) for x in sweep_obj["du_values"]],
        normalization_modes=[NormalizationMode(x) for x in sweep_obj["normalization_modes"]],
    )

    perturbation = None
    if campaign_obj.get("perturbation") is not None:
        p = campaign_obj["perturbation"]
        perturbation = PerturbationSpec(epsilon=float(p["epsilon"]), seed=int(p["seed"]))

    campaign = CampaignSpec(
        name=str(campaign_obj["name"]),
        kind=CampaignKind(campaign_obj["kind"]),
        sweep=sweep,
        spectral_control=SpectralControl(campaign_obj.get("spectral_control", "canonical")),
        perturbation=perturbation,
        shuffle_seed=campaign_obj.get("shuffle_seed"),
    )

    gates = [GateSpec(name=str(g["name"]), params=dict(g.get("params", {}))) for g in obj.get("gates", [])]
    spectral_source = str(obj.get("spectral_source", "unspecified"))

    return CampaignEnvelope(campaign=campaign, gates=gates, spectral_source=spectral_source)



def load_campaign_envelope(path: str | Path) -> CampaignEnvelope:
    return parse_campaign_envelope(json.loads(Path(path).read_text()))



def _summary_for(result: CampaignResult, params: dict[str, Any]):
    key = str(params.get("summary", "box_prime_flux"))
    try:
        return result.sweep_result.summaries[key]
    except KeyError as exc:
        raise CampaignIOError(f"missing summary key: {key}") from exc



def evaluate_gate_specs(result: CampaignResult, gates: list[GateSpec]) -> list[GateResult]:
    out: list[GateResult] = []
    for gate in gates:
        params = gate.params
        if gate.name == "stationarity":
            out.append(
                stationarity_gate(
                    _summary_for(result, params),
                    max_variance=float(params["max_variance"]),
                )
            )
        elif gate.name == "lag1_autocorrelation":
            out.append(
                autocorrelation_gate(
                    _summary_for(result, params),
                    max_abs_lag1=float(params["max_abs_lag1"]),
                )
            )
        elif gate.name == "shuffled_collapse":
            out.append(
                shuffled_collapse_gate(
                    canonical_energy=float(params["canonical_energy"]),
                    shuffled_energy=float(params["shuffled_energy"]),
                    min_ratio=float(params["min_ratio"]),
                )
            )
        elif gate.name == "perturbation_robustness":
            out.append(
                perturbation_robustness_gate(
                    canonical_energy=float(params["canonical_energy"]),
                    perturbed_energy=float(params["perturbed_energy"]),
                    max_relative_delta=float(params["max_relative_delta"]),
                )
            )
        else:
            raise CampaignIOError(f"unsupported gate: {gate.name}")
    return out
