# GitHub Actions AMD GPU Validation Demo

This project demonstrates a comprehensive CI/CD pipeline using GitHub Actions that triggers different levels of tests based on branch merging workflows. The pipeline implements a multi-stage testing strategy for code flowing from feature branches → dev branch → main branch, plus scheduled nightly runs.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Branching Strategy](#branching-strategy)
- [Workflow Overview](#workflow-overview)
- [Test Levels](#test-levels)
- [GitHub Actions Workflows](#github-actions-workflows)
- [Test Types and Markers](#test-types-and-markers)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Next Steps](#next-steps)

## 🎯 Project Overview

This is a demo project that simulates GPU driver and compute functionality for validation purposes. The project includes:

- **Mock GPU Driver** (`src/gpu_driver.py`): Simulates GPU driver operations including initialization, memory management, and compute execution
- **Mock GPU Compute Module** (`src/gpu_compute.py`): Provides workload execution and benchmarking capabilities
- **Comprehensive Test Suite**: Unit, integration, E2E, and performance tests
- **Multi-level CI/CD Pipeline**: Different test suites triggered based on branch and PR context

## 🌿 Branching Strategy

The project follows a standard Git Flow pattern:

```
feature/* → dev → main
```

### Workflow Triggers

1. **Feature Branch → Dev Branch (PR)**
   - Triggers: `pr-fast.yml` workflow
   - Fast feedback with minimal test matrix
   - Focus on code quality and unit tests
  
   <img width="500" height="445" alt="image" src="https://github.com/user-attachments/assets/ce273376-b387-4a69-a015-466ac8df64bc" />

2. **Dev Branch → Main Branch (PR)**
   - Triggers: `dev-integration.yml` workflow
   - Comprehensive integration testing
   - Medium test matrix with multiple Python/Driver combinations
   - Full security scanning
  
 <img width="500" height="400" alt="image" src="https://github.com/user-attachments/assets/ff0ce361-5612-4304-9d46-3878a7dd8e3b" />
 <img width="1024" height="247" alt="image" src="https://github.com/user-attachments/assets/7910c142-72f3-4a54-8a1a-3d0d2253846c" />
  

3. **Nightly Scheduled Runs**
   - Triggers: `nightly-full.yml` workflow (runs at 02:00 UTC daily)
   - Full test matrix across all combinations
   - Complete test suite including E2E tests
   - Comprehensive security audits and dependency checks

## 🔄 Workflow Overview

### Level 1: PR Fast Tests (Feature → Dev)

**Workflow**: `pr-fast.yml`  
**Trigger**: Pull requests targeting `main` or `dev` branches

**Tests Executed**: 
- ✅ Quality Gates (unit tests only, 100% coverage threshold)
- ✅ Unit Tests (single Python/Driver combination: Python 3.10, Driver 2.0)
- ⚠️ Quick Security Scan (non-blocking, warnings only)
Note: the number of threshold can be defined as per demand

**Characteristics**:
- Fast execution (< 5 minutes)
- Cancels previous runs on new commits
- Non-blocking security checks

### Level 2: Dev Integration Tests (Dev → Main)

**Workflow**: `dev-integration.yml`  
**Trigger**: Push to `dev` branch or PRs targeting `main`

**Tests Executed**:
- ✅ Quality Gates (unit + integration tests, 100% coverage threshold)
- ✅ Integration Tests Matrix (80% combination of Python versions × Driver versions)
- ✅ Full Security Scan
- ✅ Performance Benchmarks
Note: the number of threshold can be defined as per demand

**Test Matrix**:
- Python: 3.9, 3.10
- GPU Driver: 1.0, 2.0
- OS: ubuntu-latest

**Characteristics**:
- Medium execution time (10-20 minutes)
- Blocking security checks
- Performance validation included

### Level 3: Nightly Full Tests

**Workflow**: `nightly-full.yml`  
**Trigger**: Scheduled (daily at 02:00 UTC) or manual dispatch

**Tests Executed**:
- ✅ Full Matrix Tests (All combinations of Python versions × Driver versions)
- ✅ All Test Types (Unit + Integration + E2E)
- ✅ Performance Benchmarks
- ✅ Full Security Audit
- ✅ Dependency Check
- ✅ Quality Gates (all tests, 100% coverage threshold)

**Test Matrix**:
- Python: 3.9, 3.10, 3.11
- GPU Driver: 1.0, 2.0
- OS: ubuntu-latest

**Characteristics**:
- Comprehensive validation (30-60 minutes)
- Catches regressions across all supported configurations

## 📦 GitHub Actions Workflows

### Main Workflows

| Workflow | Purpose | Trigger |
|----------|---------|---------|
| `pr-fast.yml` | Fast PR validation | PR to main/dev |
| `dev-integration.yml` | Dev branch integration | Push to dev, PR to main |
| `nightly-full.yml` | Comprehensive nightly tests | Scheduled (daily 02:00 UTC) |

### Reusable Workflows

| Workflow | Purpose | Used By |
|----------|---------|---------|
| `test-unit.yml` | Unit test execution | pr-fast.yml, dev-integration.yml |
| `test-integration.yml` | Integration test execution | dev-integration.yml |
| `test-e2e.yml` | E2E test execution | nightly-full.yml |
| `test-matrix.yml` | Full matrix test execution | nightly-full.yml |
| `quality-gates.yml` | Code quality checks (lint, coverage, security) | pr-fast.yml, dev-integration.yml, nightly-full.yml |
| `performance-benchmark.yml` | Performance testing | dev-integration.yml, nightly-full.yml |
| `security-scan.yml` | Security scanning | dev-integration.yml |
| `security-audit.yml` | Comprehensive security audit | nightly-full.yml |
| `dependency-check.yml` | Dependency vulnerability check | nightly-full.yml |

### Supporting Workflows

| Workflow | Purpose | Trigger |
|----------|---------|---------|
| `comment-bot.yml` | PR comment automation | PR opened |
| `release.yml` | Release build | Tag push (v*) |

## 🧪 Test Types and Markers

The project uses pytest markers to categorize tests:

### Test Markers

- **`@pytest.mark.unit`**: Fast unit tests (< 1 minute)
  - Tests individual components in isolation
  - Examples: Driver initialization, memory allocation, version checks

- **`@pytest.mark.integration`**: Integration tests (5-15 minutes)
  - Tests component interactions
  - Examples: Driver + compute module integration

- **`@pytest.mark.e2e`**: End-to-end tests (15-60 minutes)
  - Tests complete workflows
  - Examples: Full workflow from initialization to compute execution

- **`@pytest.mark.performance`**: Performance benchmark tests
  - Validates latency and throughput
  - Examples: Compute performance, latency stability

- **`@pytest.mark.slow`**: Slow-running tests
  - Tests that take significant time
  - Examples: Multiple run stability tests

- **`@pytest.mark.gpu`**: Tests requiring GPU (reserved for future use)

### Test Files

| File | Test Type | Markers |
|------|-----------|---------|
| `tests/test_driver.py` | Unit + Integration | `unit`, `integration` |
| `tests/test_e2e.py` | E2E | `e2e` |
| `tests/test_performance.py` | Performance | `performance`, `unit`, `slow` |

## 📁 Project Structure

```
.
├── .github/
│   └── workflows/
│       ├── pr-fast.yml              # Fast PR tests
│       ├── dev-integration.yml      # Dev branch integration tests
│       ├── nightly-full.yml         # Nightly comprehensive tests
│       ├── test-unit.yml            # Reusable unit test workflow
│       ├── test-integration.yml     # Reusable integration test workflow
│       ├── test-e2e.yml             # Reusable E2E test workflow
│       ├── test-matrix.yml          # Reusable matrix test workflow
│       ├── quality-gates.yml        # Reusable quality gates workflow
│       ├── performance-benchmark.yml # Reusable performance workflow
│       ├── security-scan.yml        # Reusable security scan workflow
│       ├── security-audit.yml       # Reusable security audit workflow
│       ├── dependency-check.yml     # Reusable dependency check workflow
│       ├── comment-bot.yml          # PR comment automation
│       ├── release.yml              # Release build workflow
├── src/
│   ├── gpu_driver.py                # Mock GPU driver implementation
│   └── gpu_compute.py               # GPU compute module
├── tests/
│   ├── test_driver.py               # Driver unit and integration tests
│   ├── test_e2e.py                  # End-to-end tests
│   └── test_performance.py          # Performance benchmark tests
├── scripts/
│   ├── generate_matrix.py           # Dynamic test matrix generation
│   └── run_performance_test.sh      # Performance test runner script
├── pytest.ini                       # Pytest configuration
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9, 3.10, or 3.11
- pip
- pytest

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Github_Actions_amd_gpu_validation_demo-cursor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running Tests Locally

#### Run all tests:
```bash
pytest
```

#### Run specific test types:
```bash
# Unit tests only
pytest -m unit

# Integration tests
pytest -m integration

# E2E tests
pytest -m e2e

# Performance tests
pytest -m performance
```

#### Run with coverage:
```bash
pytest --cov=src --cov-report=html --cov-report=term
```

### Environment Variables

- `DRIVER_VERSION`: GPU driver version (default: "1.0", supported: "1.0", "2.0")
- `PYTHONPATH`: Python path (set automatically in CI)

### Code Quality Checks

#### Linting:
```bash
flake8 src/
black --check src/
isort --check-only src/
```

#### Security Scanning:
```bash
bandit -r src/
safety check
```

## 🔍 Workflow Details

### Quality Gates

The `quality-gates.yml` workflow performs:

1. **Linting**:
   - flake8 (code style)
   - black (formatting check)
   - isort (import sorting)

2. **Coverage**:
   - Runs tests with coverage collection
   - Generates XML and HTML reports
   - Enforces coverage thresholds (75-80% depending on workflow)
   - Uploads to Codecov

3. **Security**:
   - Bandit (SAST - Static Application Security Testing)
   - Safety (SCA - Software Composition Analysis)
   - Secret detection

### Performance Benchmarks

The `performance-benchmark.yml` workflow:
- Runs performance-marked tests
- Generates benchmark JSON reports
- Validates latency thresholds
- Uploads results as artifacts

### Security Audits

**Security Scan** (`security-scan.yml`):
- Bandit SAST scan
- Safety dependency check
- Basic secret detection

**Security Audit** (`security-audit.yml`):
- CodeQL analysis (if configured)
- Full Bandit scan
- Comprehensive Safety audit
- Extended artifact retention (90 days)

### Dependency Checks

The `dependency-check.yml` workflow:
- Safety vulnerability scanning
- pip-audit dependency checking
- Outdated package detection

## 📊 Test Execution Summary

| Stage | Workflow | Test Types | Matrix Size | Expected Run Duration | 
|-------|----------|------------|-------------|----------|
| PR (Feature→Dev) | `pr-fast.yml` | Unit | 1×1 | ~3-5 min |
| Dev Integration | `dev-integration.yml` | Unit + Integration | 2×2 | ~10-15 min |
| Nightly | `nightly-full.yml` | All (Unit + Integration + E2E) | 3×2 | ~30-60 min |

## 🎨 Features

- ✅ **Multi-level Testing**: Different test suites for different merge stages
- ✅ **Test Matrix**: Cross-platform and multi-version testing
- ✅ **Quality Gates**: Automated code quality, coverage, and security checks
- ✅ **Performance Testing**: Automated performance benchmarks
- ✅ **Security Scanning**: SAST, SCA, and secret detection
- ✅ **Dependency Management**: Automated vulnerability checking
- ✅ **Artifact Management**: Test results and reports stored as artifacts
- ✅ **Concurrency Control**: Cancels redundant workflow runs
- ✅ **Reusable Workflows**: Modular, reusable workflow components

## 📝 Notes

- The project uses mock GPU drivers suitable for CI environments without actual GPU hardware
- All workflows support manual dispatch via `workflow_dispatch`

## 🚀 Next Steps

This project currently demonstrates **Level 3-4 DevOps maturity** with solid CI/CD practices, automated testing, and quality gates. To achieve **Level 5 DevOps maturity** (Optimizing), I have identified the enhancements as TODO

### Current Maturity Assessment

**Current Level**: Level 3-4 (Defined to Quantitatively Managed)  
**Target Level**: Level 5 (Optimizing)

### Enhancement Roadmap

For detailed recommendations on advancing to Level 5 DevOps maturity:

- **Infrastructure as Code & Containerization**: Docker, Kubernetes, Terraform
- **Monitoring & Observability**: APM, distributed tracing, real-time dashboards
- **Advanced Deployment Strategies**: Blue-green, canary, automated rollbacks
- **Advanced Testing**: Contract testing, load testing, chaos engineering
- **Security Enhancements**: Runtime security, secret management, compliance automation
- **Performance Optimization**: Cost tracking, auto-scaling, resource optimization
- **Advanced CI/CD Features**: Test optimization, pipeline analytics, build optimization
- **Collaboration & Communication**: PR automation, team metrics, documentation automation

## 🔗 Related Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Markers](https://docs.pytest.org/en/stable/how-to/mark.html)
- [DevOps Enhancement Roadmap](DEVOPS_ENHANCEMENTS.md)

---

**Last Updated**: 2025-01-24

