from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class PerturbationSpec:
    epsilon: float
    seed: int


class PerturbationError(RuntimeError):
    pass



def perturb_gammas(gammas: list[float], spec: PerturbationSpec) -> list[float]:
    if spec.epsilon < 0:
        raise PerturbationError("epsilon must be nonnegative")

    rng = random.Random(spec.seed)

    perturbed = []
    for gamma in gammas:
        delta = rng.uniform(-spec.epsilon, spec.epsilon)
        perturbed.append(gamma + delta)

    return perturbed



def shuffled_gammas(gammas: list[float], seed: int) -> list[float]:
    rng = random.Random(seed)
    vals = list(gammas)
    rng.shuffle(vals)
    return vals



def truncation_family(gammas: list[float], truncations: list[int]) -> dict[int, list[float]]:
    return {n: gammas[:n] for n in truncations}
