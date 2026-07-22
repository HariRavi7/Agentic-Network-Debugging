"""
Domain IP Resolver - Simple JSON output for LLM tool use.

Resolves a domain to its IP addresses with a single call
and returns all unique IPs in a clean, easy-to-read JSON response.
"""

import socket
from typing import Optional


def resolve_domain_ip(domain: str) -> Optional[dict]:
    """
    Resolve a domain name to all its IP addresses.

    Makes a single getaddrinfo call to retrieve all IPv4 and IPv6
    addresses associated with the domain.

    Args:
        domain: The domain name to resolve (e.g., "example.com").

    Returns:
        A simple JSON dict with:
            - domain: The domain queried.
            - ips: A list of all resolved IP addresses.
        Returns None if resolution fails.
    """
    try:
        # Single call — no family/sock_type filter, gets everything
        raw = socket.getaddrinfo(domain, 0)
    except socket.gaierror as e:
        print(f"Error resolving domain {domain}: {e}")
        return None

    # Deduplicate IPs across all returned address entries
    ips = sorted(set(entry[4][0] for entry in raw))

    return {
        "domain": domain,
        "ips": ips,
    }


if __name__ == "__main__":
    result = resolve_domain_ip("example.com")
    if result:
        import json
        print(json.dumps(result, indent=2))
    else:
        print("Resolution failed.")

