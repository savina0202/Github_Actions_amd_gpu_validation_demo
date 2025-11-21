"""
End-to-end tests for the GPU validation system.
These tests verify the complete workflow from initialization to compute execution.
"""
import pytest
import os
from src.gpu_driver import GPUDriver
from src.gpu_compute import run_workload, benchmark_compute


@pytest.mark.e2e
def test_full_workflow():
    """
    E2E test: Complete workflow from driver initialization to compute execution.
    """
    # Initialize driver
    driver = GPUDriver()
    driver.initialize()
    assert driver.initialized is True
    
    # Allocate memory
    allocated = driver.allocate_memory(512)
    assert allocated == 512
    
    # Run compute
    result = driver.run_compute(100)
    assert result == 200
    
    # Run workload through compute module
    workload_result = run_workload(50)
    assert workload_result == 100
    
    # Benchmark performance
    output, latency = benchmark_compute(200)
    assert output == 400
    assert latency < 0.2  # Performance check
    
    # Release memory
    released = driver.release_memory(256)
    assert released == 256


@pytest.mark.e2e
def test_driver_version_workflow():
    """
    E2E test: Verify driver version affects workflow behavior.
    """
    driver = GPUDriver()
    
    # Set driver version via environment variable
    original_version = os.getenv("DRIVER_VERSION")
    os.environ["DRIVER_VERSION"] = "2.0"
    
    driver2 = GPUDriver()
    driver2.initialize()
    
    version = driver2.get_version()
    assert version == "2.0"
    
    # Temperature should differ based on version
    temp = driver2.get_temperature()
    assert 45 <= temp <= 60  # Version 2.0 has base temp 50
    
    # Restore original version if it existed
    if original_version:
        os.environ["DRIVER_VERSION"] = original_version

