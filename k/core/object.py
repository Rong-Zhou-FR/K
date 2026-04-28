from __future__ import annotations

import uuid
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from k.core.state import State, Vector3T


class PhysicalObject:
    def __init__(
        self,
        shape: str,
        state: State,
        id: str | None = None,
    ) -> None:
        self.id = id or uuid.uuid4().hex[:8]
        self.state = state
        self.shape = shape

    def apply(self, influence: object) -> None:
        if hasattr(influence, "force"):
            self.state.forces.append((influence.force, influence.point))
        elif hasattr(influence, "torque"):
            self.state.torques.append(influence.torque)
        elif hasattr(influence, "heat_rate"):
            self.state.heat_flows.append((influence.heat_rate, influence.location))

    def enable_domain(self, domain: str) -> None:
        self.state.enabled_domains.add(domain)

    def disable_domain(self, domain: str) -> None:
        self.state.enabled_domains.discard(domain)

    def __repr__(self) -> str:
        return f"PhysicalObject(id={self.id!r}, shape={self.shape!r})"
