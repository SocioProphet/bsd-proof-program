from m1.perturbation import (
    PerturbationSpec,
    perturb_gammas,
    shuffled_gammas,
    truncation_family,
)



def test_perturbation_changes_values():
    gammas = [1.0, 2.0, 3.0]

    out = perturb_gammas(gammas, PerturbationSpec(epsilon=0.1, seed=1))

    assert out != gammas
    assert len(out) == len(gammas)



def test_shuffle_preserves_multiset():
    gammas = [1.0, 2.0, 3.0]

    out = shuffled_gammas(gammas, seed=1)

    assert sorted(out) == sorted(gammas)



def test_truncation_family():
    gammas = [1.0, 2.0, 3.0, 4.0]

    fam = truncation_family(gammas, [1, 3])

    assert fam[1] == [1.0]
    assert fam[3] == [1.0, 2.0, 3.0]
