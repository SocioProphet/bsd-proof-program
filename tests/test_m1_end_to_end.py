from pathlib import Path

from m1.li_quadrature import QuadratureConfig, constant_integral_closed_form, trapezoid_integral
from m1.manifest import BoxRecord, FrozenManifestWriter, Manifest
from m1.psi_residual import compute_residual
from m1.sieve import prime_count


def test_trapezoid_closed_form_consistency():
    cfg = QuadratureConfig(du=0.001)

    approx = trapezoid_integral(lambda u: 1.0, 0.0, 1.0, cfg)

    assert abs(approx - 1.0) < 1e-3



def test_closed_form_log_interval():
    val = constant_integral_closed_form(10, 100)
    assert abs(val - 2.30258509299) < 1e-9



def test_m1_pipeline_smoke(tmp_path: Path):
    interval = (1000, 1100)

    count = prime_count(*interval)

    cfg = QuadratureConfig(du=0.0025)

    r1 = compute_residual(interval[0], interval[1], [14.134725141734693790], cfg)
    r2 = compute_residual(
        interval[0],
        interval[1],
        [
            14.134725141734693790,
            21.022039638771554993,
            25.010857580145688763,
        ],
        cfg,
    )

    assert r1.truncation_level == 1
    assert r2.truncation_level == 3

    manifest = Manifest(
        interval=interval,
        resolution_du=cfg.du,
        zero_table_sha256="deadbeef",
        boxes=[
            BoxRecord(
                left=interval[0],
                right=interval[1],
                prime_count=count,
                psi_increment=r1.psi_increment,
            )
        ],
        residuals=[r1, r2],
    )

    out = tmp_path / "manifest.json"

    digest = FrozenManifestWriter.write(out, manifest)

    assert out.exists()
    assert len(digest) == 64
