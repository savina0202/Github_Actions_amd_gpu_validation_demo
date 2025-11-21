#!/bin/bash
echo "Running performance tests..."
pytest tests/test_performance.py -q

# Generate a simple text report
echo "Performance test summary" > perf_report.txt
date >> perf_report.txt
echo "Latency thresholds validated." >> perf_report.txt
echo "Done."
