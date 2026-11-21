# Test Strategy

## Scope

The current tests exercise three deterministic input-validation functions. They do not test network connectivity, cloud APIs, external services or production infrastructure.

## Test categories

| Category | Examples |
|---|---|
| Happy path | Valid IPv4 CIDRs, ports and hostnames |
| Boundary | IPv4 /0 and /32; ports 1 and 65535; DNS label length |
| Invalid format | Malformed CIDR, empty hostname, invalid DNS label |
| Type validation | Boolean, float, string or null where an integer is required |
| Explicit behavior | IPv6 rejection; strict versus non-strict network parsing |
| Normalization | Hostname lowercasing and trailing-dot handling |

## Running tests

```bash
python -m pip install -e ".[test]"
python -m pytest
```

## Test design principles

- Keep tests deterministic and independent of network access.
- Use synthetic documentation-range IP addresses.
- Assert the specific exception category for invalid input.
- Parameterize related cases without hiding the intent of each test.
- Avoid asserting implementation details when a public behavior is sufficient.

## Future additions

- Property-based tests for generated IPv4 prefixes and DNS labels.
- Mutation testing to identify weak assertions.
- API contract tests using local fixtures.
- Coverage reporting and type checking as independent quality gates.
