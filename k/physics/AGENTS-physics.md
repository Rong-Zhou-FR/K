# AGENTS-physics.md — Physics Domains Agent Instructions

## Summary

Parent file for all physics domain modules. Contains shared conventions and cross-domain integration rules.

## Purpose and Expected Behavior

Organizes physics modules:
- `mechanics/` - Classical mechanics
- `thermodynamics/` - Thermal physics
- `electromagnetism/` - EM fields
- `optics/` - Light/optics
- `fluid/` - Fluid dynamics

## Shared Conventions

- All physics calculations use SI units
- Time in seconds (s)
- Temperature in Kelvin (K)
- Mass in kilograms (kg)

## Cross-Domain Integration

Physics domains interact via `core/State`:

```python
from numpy.typing import NDArray

# Example: Thermo-mechanical coupling
@dataclass
class State:
    # Mechanics (always present)
    position: NDArray[np.float64]
    velocity: NDArray[np.float64]

    # Thermodynamics (if enabled)
    temperature: float = 298.15

    # Electromagnetism (if enabled)
    charge: float = 0.0

    # Domain flags
    enabled_domains: set[str] = {"mechanics"}
```

## Constraints

- New domains must implement `PhysicsPlugin` protocol
- Domain-specific State fields must have defaults
- Cross-domain effects documented explicitly

## Domain-Specific Rules for Agents

- Add new domain: Create `k/physics/[domain]/AGENTS-[domain].md`
- Update this file's table when adding domains
- Follow inheritance from `AGENTS.md`
