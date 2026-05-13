from m1.chebyshev import chebyshev_psi_increment
from m1.li_quadrature import QuadratureConfig
from m1.psi_residual import compute_residual, psi_increment



def test_psi_increment_uses_chebyshev_engine():
    assert psi_increment(10, 100) == chebyshev_psi_increment(10, 100)



def test_zero_truncation_residual_equals_raw_psi_increment():
    result = compute_residual(10, 100, [], QuadratureConfig(du=0.01))

    assert result.truncation_level == 0
    assert result.channel_sum == 0.0
    assert result.residual == result.psi_increment
