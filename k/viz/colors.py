from __future__ import annotations

from typing import Final

from k.core.object import PhysicalObject

DOMAIN_COLORS: Final[dict[str, str]] = {
    "mechanics": "#1f77b4",
    "thermodynamics": "#ff7f0e",
    "electromagnetism": "#2ca02c",
    "optics": "#d62728",
    "fluid": "#9467bd",
}


def get_domain_color(domain: str) -> str:
    return DOMAIN_COLORS.get(domain, "#333333")


def get_object_color(obj: PhysicalObject) -> str:
    if obj.state.enabled_domains:
        return get_domain_color(next(iter(obj.state.enabled_domains)))
    return "#333333"
