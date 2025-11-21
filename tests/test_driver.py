import pytest
from src.gpu_driver import GPUDriver
from src.gpu_compute import run_workload

# Test cases for GPUDriver functionalities
@pytest.mark.unit
def test_driver_initialization():
    driver = GPUDriver()
    msg = driver.initialize()
    assert "initialized" in msg
    assert driver.initialized is True


@pytest.mark.unit
def test_driver_version():
    driver = GPUDriver()
    assert driver.get_version() in ["1.0", "2.0"]


@pytest.mark.unit
def test_memory_allocation():
    driver = GPUDriver()
    driver.initialize()

    allocated = driver.allocate_memory(256)
    assert allocated == 256

    allocated = driver.allocate_memory(128)
    assert allocated == 384

    released = driver.release_memory(128)
    assert released == 256


@pytest.mark.integration
def test_compute_pipeline():
    """Integration test: driver and compute module working together"""
    driver = GPUDriver()
    driver.initialize()

    result = driver.run_compute(10)
    assert result == 20  # Mock compute logic

    # Also test via compute module
    workload_result = run_workload(5)
    assert workload_result == 10
