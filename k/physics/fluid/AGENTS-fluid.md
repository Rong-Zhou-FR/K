# AGENTS-fluid.md — Fluid Dynamics Agent Instructions

## Summary

Fluid dynamics module (basic): fluid properties, hydrostatics, and simple flow.

## Purpose and Expected Behavior

Basic fluid calculations:
- Fluid properties (density, viscosity, pressure)
- Hydrostatic pressure
- Buoyancy (Archimedes' principle)
- Simple flow (optional)

## Constraints and Invariants

- All fluid calculations use SI units
- Density: kg/m³
- Pressure: Pascals (Pa)
- Dynamic viscosity: Pa·s
- Kinematic viscosity: m²/s

## Key Classes

```python
class Fluid:
    density: float  # kg/m³
    dynamic_viscosity: float  # Pa·s

class FluidObject(PhysicalObject):
    # Object immersed in fluid
    fluid: Fluid

def hydrostatic_pressure(rho: float, g: float, h: float) -> float: ...
def buoyancy(rho_fluid: float, V_displaced: float, g: float) -> float: ...
def reynolds_number(rho: float, v: float, L: float, mu: float) -> float: ...
```

## Documentation Reference

- `docs/man/physics/fluid/index.md`
- `docs/man/physics/fluid/hydrostatics.md`

## Integration Points

- Connected to `physics/mechanics` for forces
- Optional backend: Full CFD libraries for advanced flow

## Domain-Specific Rules for Agents

- Keep basic (educational level) - full CFD too complex for core
- Focus on hydrostatics and buoyancy first
- Flow calculations optional