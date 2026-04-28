# AGENTS-thermodynamics.md — Thermodynamics Agent Instructions

## Summary

Thermal physics module: heat transfer, temperature, thermal properties, and heat sources.

## Purpose and Expected Behavior

Heat calculations based on thermodynamic principles:
- Temperature tracking and updates
- Heat conduction, convection, radiation
- Specific heat capacity
- Thermal equilibrium
- Heat source/sink management

## Constraints and Invariants

- All thermodynamics calculations use SI units
- Temperature in Kelvin (K)
- Heat in Joules (J)
- Power in Watts (W)
- Thermal conductivity: W/(m·K)

## Key Classes

```python
from numpy.typing import NDArray

class HeatSource:
    temperature: float  # Kelvin
    power: float  # Watts
    location: NDArray[np.float64]

class ThermalObject(PhysicalObject):
    # Adds thermal properties to PhysicalObject
    temperature: float
    heat_capacity: float  # J/(kg·K)
    thermal_conductivity: float  # W/(m·K)

def heat_conduction(obj_a: ThermalObject, obj_b: ThermalObject, dt: float) -> float: ...
def newtons_cooling(obj: ThermalObject, ambient: float, dt: float) -> float: ...
def update_temperature(obj: ThermalObject, dt: float) -> None: ...
```

## Documentation Reference

- `docs/man/physics/thermodynamics/index.md`
- `docs/man/physics/thermodynamics/heat_transfer.md`

## Integration Points

- Connected to `core/State` for temperature field
- Optional backend: `coolprop` for thermophysical properties

## Domain-Specific Rules for Agents

- Temperature never below absolute zero (0 K)
- Heat flow direction: hot → cold
- Implement all three heat transfer modes: conduction, convection, radiation