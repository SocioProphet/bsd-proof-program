from m1.statistics import (
    aggregate_box_residuals,
    scaling_slope,
    summarize_stationarity,
)



def test_stationarity_summary():
    vals = [1.0, -1.0, 1.0, -1.0]

    summary = summarize_stationarity(vals)

    assert summary.count == 4
    assert summary.energy > 0



def test_block_aggregation():
    vals = [1.0, 2.0, 3.0, 4.0]

    agg = aggregate_box_residuals(vals, 2)

    assert agg == [1.5, 3.5]



def test_scaling_slope_positive():
    xs = [10.0, 100.0, 1000.0]
    ys = [1.0, 10.0, 100.0]

    slope = scaling_slope(xs, ys)

    assert slope > 0.5
