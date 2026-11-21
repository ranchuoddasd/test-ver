"""Small deterministic input validators used by the testing examples."""

from __future__ import annotations

import ipaddress
import re
from typing import Union

IPv4Network = ipaddress.IPv4Network
IPAddressInput = Union[str, IPv4Network]

_HOST_LABEL = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")


def parse_ipv4_network(value: IPAddressInput, *, strict: bool = True) -> IPv4Network:
    """Parse an IPv4 network; reject IPv6 and malformed values.

    Args:
        value: IPv4 CIDR text or an IPv4Network instance.
        strict: When True, require all host bits to be zero.

    Raises:
        TypeError: If value is not text or an IPv4Network.
        ValueError: If value is not a valid IPv4 network.
    """
    if isinstance(value, IPv4Network):
        if strict and value != IPv4Network((value.network_address, value.prefixlen), strict=True):
            raise ValueError("Network contains host bits")
        return value
    if not isinstance(value, str):
        raise TypeError("value must be an IPv4 CIDR string or IPv4Network")
    try:
        network = ipaddress.ip_network(value.strip(), strict=strict)
    except ValueError as exc:
        raise ValueError(f"Invalid IPv4 network: {value!r}") from exc
    if not isinstance(network, IPv4Network):
        raise ValueError("IPv6 networks are not supported")
    return network


def validate_port(value: int) -> int:
    """Return a TCP/UDP port number in the inclusive range 1–65535."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("port must be an integer")
    if not 1 <= value <= 65535:
        raise ValueError("port must be between 1 and 65535")
    return value


def normalize_hostname(value: str) -> str:
    """Validate and lowercase a DNS-style hostname.

    A single trailing dot is accepted and removed. Underscores, empty labels,
    labels longer than 63 characters and total names longer than 253
    characters are rejected.
    """
    if not isinstance(value, str):
        raise TypeError("hostname must be a string")

    hostname = value[:-1] if value.endswith(".") else value
    hostname = hostname.lower()
    if not hostname or len(hostname) > 253:
        raise ValueError("hostname must contain 1–253 characters")
    labels = hostname.split(".")
    if any(not _HOST_LABEL.fullmatch(label) for label in labels):
        raise ValueError("hostname contains an invalid DNS label")
    return hostname
