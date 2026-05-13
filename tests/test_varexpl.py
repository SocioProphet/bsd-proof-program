from m1.varexpl import variance_explained



def test_variance_explained_improves():
    raw = [10.0, 12.0, 8.0, 11.0, 9.0]
    residual = [1.0, 0.5, -0.5, 0.75, -0.25]

    result = variance_explained(raw, residual)

    assert result.explained_fraction > 0
    assert result.residual_variance < result.raw_variance
