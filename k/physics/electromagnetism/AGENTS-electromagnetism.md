# AGENTS-electromagnetism.md — Electromagnetism Agent Instructions

## Summary

Electromagnetism module: electric fields, magnetic fields, charges, and EM sources.

## Purpose and Expected Behavior

EM calculations based on Maxwell's equations:
- Electric field calculation (Coulomb's law)
- Magnetic field calculation (Biot-Savart)
- Lorentz force on charged particles
- EM wave propagation (optional)

## Constraints and Invariants

- All EM calculations use SI units
- Charge: Coulombs (C)
- Electric field: Volts/meter (V/m)
- Magnetic field: Tesla (T)
- Permittivity: ε₀ = 8.854×10⁻¹² F/m
- Permeability: μ₀ = 4π×10⁻⁷ H/m

## Key Classes

```python
from numpy.typing import NDArray

class Charge:
    value: float  # Coulombs
    position: NDArray[np.float64]

class ElectricField:
    direction: NDArray[np.float64]
    magnitude: float

class MagneticField:
    direction: NDArray[np.float64]
    magnitude: float

class EMObject(PhysicalObject):
    # Adds EM properties
    charge: float
    current: NDArray[np.float64]

def electric_field(point_charge: Charge, position: NDArray[np.float64]) -> NDArray[np.float64]: ...
def magnetic_field(wire_segment: NDArray[np.float64], position: NDArray[np.float64]) -> NDArray[np.float64]: ...
def lorentz_force(charge: float, E: NDArray[np.float64], v: NDArray[np.float64], B: NDArray[np.float64]) -> NDArray[np.float64]: ...
```

## Documentation Reference

- `docs/man/physics/electromagnetism/index.md`
- `docs/man/physics/electromagnetism/fields.md`

## Domain-Specific Rules for Agents

- Use vectorized numpy operations for field calculations
- Support point charges and continuous charge distributions
- Implement superposition principle explicitly
- Handle relativistic effects as optional extension