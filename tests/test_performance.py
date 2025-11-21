import time
import pytest
from src.gpu_compute import benchmark_compute


@pytest.mark.performance
@pytest.mark.unit
def test_compute_performance():
    """
    Mock performance test.
    Ensures workload latency is within an acceptable range.
    """

    output, latency = benchmark_compute(100)

    # Validate compute output
    assert output == 200

    # Validate latency (mock threshold, ~0.1s)
    assert latency < 0.2  # Avoid flakiness in CI


@pytest.mark.performance
@pytest.mark.slow
def test_multiple_runs_latency_stability():
    """
    Ensure latency does not fluctuate too much across runs.
    """
    latencies = []
    for _ in range(5):
        _, latency = benchmark_compute(50)
        latencies.append(latency)

    avg = sum(latencies) / len(latencies)

    # Ensure latency stability
    for l in latencies:
        assert abs(l - avg) < 0.15
