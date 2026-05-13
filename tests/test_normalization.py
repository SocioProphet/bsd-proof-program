import math

from m1.normalization import (
    NormalizationMode,
    normalize_all_modes,
    normalize_residual,
    prime_flux_scale,
)



def test_all_normalizations_present():
    vals = normalize_all_modes(10.0, 100, 200)
    assert len(vals) == 4



def test_log_volume_positive():
    r = normalize_residual(5.0, 100, 200, NormalizationMode.LOG_VOLUME)
    assert r.scale > 0



def test_prime_flux_scale_matches_formula():
    scale = prime_flux_scale(100, 200)

    u = 0.5 * (math.log(100) + math.log(200))
    expected = math.exp(u) / u

    assert abs(scale - expected) < 1e-12
