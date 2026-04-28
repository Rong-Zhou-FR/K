# K - 3D Classical Physics Library

**K** is a Python library for 3D classical physics simulation, calculation, and visualization — covering all major branches of classical physics.

## Features

- **Comprehensive**: Mechanics, thermodynamics, electromagnetism, optics, fluid dynamics
- **Modular**: Enable only the physics domains you need
- **Educational**: Built for grade-school to bachelor's level
- **100% FOSS**: Zero proprietary dependencies
- **Lightweight**: Minimal dependencies, pure Python core
- **Extensible**: Plugin architecture for custom physics

## Installation

```bash
pip install k
```

## Quick Start

```python
import k

# Create 3D space with mechanics enabled
space = k.Space(dimensions=3, domains=["mechanics", "thermodynamics"])

# Add a box
box = k.Object(shape="box", dimensions=[1, 1, 1], mass=2.0, position=[0, 0, 5])
space.add(box)

# Apply gravity
box.apply(k.Force(vector=[0, 0, -9.8 * box.mass]))

# Simulate
solver = k.Solver(space=space, dt=0.01)
solver.run(duration=10)

# Visualize
k.viz.show(space)
```

## Physics Domains

| Domain | Description |
|--------|-------------|
| `mechanics` | Rigid bodies, forces, collisions |
| `thermodynamics` | Heat transfer, temperature |
| `electromagnetism` | Electric & magnetic fields |
| `optics` | Ray tracing, lenses, mirrors |
| `fluid` | Hydrostatics, buoyancy |

## Tech Stack

| Component | Library |
|-----------|---------|
| Computation | NumPy, SciPy |
| 2D Viz | Matplotlib |
| 3D Viz | PyVista |

## Documentation

Coming soon.

## License

AGPL 3.0
