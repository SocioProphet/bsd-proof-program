from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from m1.experiments import SweepResult, SweepSpec, run_sweep
from m1.perturbation import PerturbationSpec, perturb_gammas, shuffled_gammas


class CampaignKind(str, Enum):
    CANONICAL = "canonical"
    NULL_MODEL = "null_model"
    PERTURBATION = "perturbation"
    NORMALIZATION_COMPARISON = "normalization_comparison"


class SpectralControl(str, Enum):
    CANONICAL = "canonical"
    PERTURBED = "perturbed"
    SHUFFLED = "shuffled"


@dataclass(frozen=True)
class CampaignSpec:
    name: str
    kind: CampaignKind
    sweep: SweepSpec
    spectral_control: SpectralControl = SpectralControl.CANONICAL
    perturbation: PerturbationSpec | None = None
    shuffle_seed: int | None = None


@dataclass(frozen=True)
class CampaignResult:
    campaign: CampaignSpec
    sweep_result: SweepResult
    spectral_control: SpectralControl


class CampaignError(RuntimeError):
    pass



def _controlled_gammas(spec: CampaignSpec, gammas: list[float]) -> list[float]:
    if spec.spectral_control == SpectralControl.CANONICAL:
        return gammas

    if spec.spectral_control == SpectralControl.PERTURBED:
        if spec.perturbation is None:
            raise CampaignError("perturbed campaign requires perturbation spec")
        return perturb_gammas(gammas, spec.perturbation)

    if spec.spectral_control == SpectralControl.SHUFFLED:
        if spec.shuffle_seed is None:
            raise CampaignError("shuffled campaign requires shuffle_seed")
        return shuffled_gammas(gammas, spec.shuffle_seed)

    raise CampaignError(f"unsupported spectral control: {spec.spectral_control}")



def run_campaign(spec: CampaignSpec, gammas: list[float]) -> CampaignResult:
    controlled = _controlled_gammas(spec, gammas)
    result = run_sweep(spec.sweep, controlled)
    return CampaignResult(
        campaign=spec,
        sweep_result=result,
        spectral_control=spec.spectral_control,
    )
