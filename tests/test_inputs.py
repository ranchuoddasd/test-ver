import ipaddress

import pytest

from validation_lab.inputs import (
    normalize_hostname,
    parse_ipv4_network,
    validate_port,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("192.0.2.0/24", ipaddress.IPv4Network("192.0.2.0/24")),
        ("198.51.100.7/32", ipaddress.IPv4Network("198.51.100.7/32")),
        ("0.0.0.0/0", ipaddress.IPv4Network("0.0.0.0/0")),
    ],
)
def test_parse_ipv4_network_valid(value, expected):
    assert parse_ipv4_network(value) == expected


@pytest.mark.parametrize("value", ["192.0.2.1/24", "not-a-network", "192.0.2.0/33", "2001:db8::/32"])
def test_parse_ipv4_network_rejects_invalid_or_ipv6(value):
    with pytest.raises(ValueError):
        parse_ipv4_network(value)


def test_parse_ipv4_network_can_allow_host_bits_when_non_strict():
    assert parse_ipv4_network("192.0.2.7/24", strict=False) == ipaddress.IPv4Network("192.0.2.0/24")


def test_parse_ipv4_network_rejects_wrong_input_type():
    with pytest.raises(TypeError):
        parse_ipv4_network(123)  # type: ignore[arg-type]


@pytest.mark.parametrize("port", [1, 22, 443, 65535])
def test_validate_port_accepts_boundaries_and_common_ports(port):
    assert validate_port(port) == port


@pytest.mark.parametrize("port", [0, -1, 65536])
def test_validate_port_rejects_out_of_range_values(port):
    with pytest.raises(ValueError):
        validate_port(port)


@pytest.mark.parametrize("port", [True, False, "443", 443.0, None])
def test_validate_port_rejects_non_integer_values(port):
    with pytest.raises(TypeError):
        validate_port(port)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("Example.COM", "example.com"),
        ("api.example.com.", "api.example.com"),
        ("node-1.lab.example", "node-1.lab.example"),
    ],
)
def test_normalize_hostname_valid(value, expected):
    assert normalize_hostname(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "",
        ".",
        "-bad.example",
        "bad-.example",
        "bad..example",
        "has space.example",
        "_service.example",
        "a" * 64 + ".example",
        "a" * 254,
    ],
)
def test_normalize_hostname_rejects_invalid_names(value):
    with pytest.raises(ValueError):
        normalize_hostname(value)


def test_normalize_hostname_rejects_wrong_input_type():
    with pytest.raises(TypeError):
        normalize_hostname(None)  # type: ignore[arg-type]
