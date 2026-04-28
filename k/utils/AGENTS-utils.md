# AGENTS-utils.md — Utilities Agent Instructions

## Summary

Utilities: physical constants, unit handling, and I/O operations.

## Purpose and Expected Behavior

Helper functionality:
- Physical constants (c, g, G, etc.)
- Unit conversion utilities
- Import/export (JSON, HDF5)
- Logging configuration

## Constraints and Invariants

- Constants must be numpy arrays or floats
- Units: SI by default, conversions available
- I/O: JSON for small data, HDF5 for large simulations

## Key Modules

```python
# k/utils/constants.py
SPEED_OF_LIGHT: float = 299792458.0
GRAVITATIONAL_CONSTANT: float = 6.67430e-11
STANDARD_GRAVITY: float = 9.80665
PERMITTIVITY_VACUUM: float = 8.854e-12
PERMEABILITY_VACUUM: float = 4 * pi * 1e-7

# k/utils/units.py
def convert(value: float, from_unit: str, to_unit: str) -> float: ...
def to_si(value: float, unit: str) -> float: ...
def from_si(value: float, unit: str) -> float: ...
```

## Documentation Reference

- `docs/man/utils/constants.md`
- `docs/man/utils/units.md`

## Domain-Specific Rules for Agents

- SI units as internal representation
- Document units in function signatures
- Constants immutable (use UPPER_SNAKE_CASE)
- I/O functions must handle None gracefully