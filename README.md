# Validation Testing Lab

A small, reproducible Python project demonstrating input validation, boundary testing, parameterized unit tests and continuous integration.

**Status:** Learning and portfolio project. The examples are deterministic local validators; they are not a production validation service.

## Objectives

- Demonstrate clear validation contracts and predictable exceptions.
- Cover valid inputs, invalid inputs and boundary conditions.
- Use pytest parameterization to keep test cases readable.
- Run the test suite automatically with GitHub Actions.

## Implemented examples

- IPv4 network parsing with explicit IPv4-only behavior and configurable strictness.
- TCP/UDP port validation for the valid range 1–65535.
- Hostname normalization and validation for DNS-style hostnames.

## Repository structure

```text
.
├── pyproject.toml
├── src/
│   └── validation_lab/
│       ├── __init__.py
│       └── inputs.py
├── tests/
│   └── test_inputs.py
├── docs/
│   ├── planning.md
│   └── test-strategy.md
└── .github/
    └── workflows/
        └── tests.yml
```

## Requirements

- Python 3.10+
- pytest (installed through the optional `test` dependency group)

## Setup and run

```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

python -m pip install -e ".[test]"
python -m pytest
```

## Validation contracts

| Function | Contract |
|---|---|
| `parse_ipv4_network` | Returns an IPv4Network; rejects malformed input and IPv6 |
| `validate_port` | Returns a valid integer port; rejects booleans, non-integers and values outside 1–65535 |
| `normalize_hostname` | Returns a lowercase DNS-style hostname; rejects invalid labels and total lengths |

Invalid values raise `ValueError` (or `TypeError` for values of the wrong Python type, where documented by the implementation).

## Test approach

The suite uses parameterized tests for normal values, boundaries and invalid inputs. See [docs/test-strategy.md](docs/test-strategy.md) for coverage categories and extension guidance.

## Continuous integration

The GitHub Actions workflow installs the project and runs pytest on pushes and pull requests. A green workflow indicates that the checked-in tests passed in that CI run; it does not establish production readiness or exhaustive correctness.

## Security and data handling

All examples are local and deterministic. Do not add real credentials, internal hostnames, customer network ranges, private endpoints or production configuration to this public repository.

## Roadmap

1. Add property-based testing for network and hostname edge cases.
2. Add JSON schema and API payload validation examples.
3. Add mutation testing to evaluate test effectiveness.
4. Add coverage reporting with an explicitly stated threshold.
5. Add static analysis and type checking as separate CI jobs.

## License

No license is currently provided. Until a license is added, reuse and redistribution are not granted by default.
