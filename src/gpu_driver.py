import time
import random
import os


class GPUDriver:
    """
    A mock GPU driver that simulates basic driver functionality.
    Suitable for CI pipelines where no GPU exists.
    """

    def __init__(self):
        self.version = os.getenv("DRIVER_VERSION", "1.0")
        self.initialized = False
        self.memory_allocated = 0

    # Initialize the driver
    def initialize(self):
        """Simulate driver initialization."""
        time.sleep(0.1)
        self.initialized = True
        return f"Driver {self.version} initialized."

    # Get driver version
    def get_version(self):
        """Return driver version."""
        return self.version

    # Memory management
    def allocate_memory(self, amount):
        """Simulate memory allocation."""
        if not self.initialized:
            raise RuntimeError("Driver not initialized")
        self.memory_allocated += amount
        return self.memory_allocated

    # Free memory
    def release_memory(self, amount):
        """Simulate memory free."""
        self.memory_allocated = max(self.memory_allocated - amount, 0)
        return self.memory_allocated

    # Get temperature
    def get_temperature(self):
        """Return a fake temperature."""
        # Different driver versions behave differently
        base_temp = 45 if self.version == "1.0" else 50
        #Fixed bug#3 2025-11-23
        return base_temp + random.randint(0, 5)

    def run_compute(self, workload_size):
        """Forward computation to compute engine."""
        if not self.initialized:
            raise RuntimeError("Driver not initialized")
        time.sleep(0.1)
        return workload_size * 2  # Just a mock result
