import time
import random


def run_workload(size):
    """
    Simulate a GPU workload.
    For CI pipelines we only emulate latency and output.
    """
    # Simulate variable computation time
    time.sleep(0.05 + random.random() * 0.05)

    # Fake compute result (e.g., doubling the input size)
    result = size * 2
    return result


def benchmark_compute(size):
    """
    Benchmark compute time for performance testing
    """
    start = time.time()
    output = run_workload(size)
    end = time.time()
    latency = end - start
    return output, latency
