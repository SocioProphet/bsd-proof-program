from pathlib import Path

import pytest

from m1.campaign_io import evaluate_gate_specs, load_campaign_envelope, load_gammas
from m1.campaigns import run_campaign
from m1.experiments import ExperimentError


SPEC_TEXT = """
{
  "spectral_source": "test_source",
  "campaign": {
    "name": "io-smoke",
    "kind": "canonical",
    "spectral_control": "canonical"
  },
  "sweep": {
    "name": "io-sweep",
    "intervals": [
      {"name": "T", "left": 10, "right": 100, "du": 0.01}
    ],
    "truncation_levels": [0, 1],
    "du_values": [0.01],
    "normalization_modes": ["box_prime_flux"]
  },
  "gates": [
    {
      "name": "stationarity",
      "params": {
        "summary": "box_prime_flux",
        "max_variance": 1e30
      }
    }
  ]
}
"""



def test_campaign_json_load_and_gate_application(tmp_path: Path):
    spec_path = tmp_path / "spec.json"
    gamma_path = tmp_path / "gammas.txt"

    spec_path.write_text(SPEC_TEXT)
    gamma_path.write_text("14.134725141734693790\n")

    envelope = load_campaign_envelope(spec_path)
    gammas = load_gammas(gamma_path)
    result = run_campaign(envelope.campaign, gammas)
    gates = evaluate_gate_specs(result, envelope.gates)

    assert envelope.spectral_source == "test_source"
    assert len(result.sweep_result.observations) == 2
    assert len(gates) == 1



def test_campaign_requires_enough_gammas(tmp_path: Path):
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(SPEC_TEXT)
    envelope = load_campaign_envelope(spec_path)

    with pytest.raises(ExperimentError):
        run_campaign(envelope.campaign, [])
