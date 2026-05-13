import math

from m1.chebyshev import (
    chebyshev_psi,
    chebyshev_psi_increment,
    von_mangoldt,
)



def test_von_mangoldt_prime():
    assert abs(von_mangoldt(13) - math.log(13)) < 1e-12



def test_von_mangoldt_prime_power():
    assert abs(von_mangoldt(27) - math.log(3)) < 1e-12



def test_von_mangoldt_non_prime_power():
    assert von_mangoldt(12) == 0.0



def test_chebyshev_psi_monotone():
    assert chebyshev_psi(100) >= chebyshev_psi(50)



def test_chebyshev_increment_positive():
    assert chebyshev_psi_increment(100, 200) > 0
