# K - 3D Classical Physics Simulation Library

## 0. Project Vision & Differentiation

### Why K Exists

**Existing libraries (PyChrono, Newton, DART, etc.) cover**:

- Mechanics only (mostly robotics/vehicle-focused)
- Single physics domain
- Engineering/research use cases

**K covers**:

- **All domains of classical physics** (mechanics, thermodynamics, electromagnetism, optics, fluid dynamics)
- **Educational focus** — grade-school to bachelor's degree level
- **Modular selection** — user enables only needed domains
- **Lightweight & pure Python** — minimal dependencies, build core from scratch for transparency

### Comparison with Existing Libraries

| Feature | PyChrono | Newton | DART | **K** |
|---------|----------|--------|------|-------|
| Mechanics | ✓ | ✓ | ✓ | ✓ |
| Thermodynamics | ✗ | ✗ | ✗ | ✓ |
| Electromagnetism | ✗ | ✗ | ✗ | ✓ |
| Optics | ✗ | ✗ | ✗ | ✓ |
| Fluid (basic) | ✓ | ✗ | ✗ | ✓ |
| Educational focus | ✗ | ✗ | ✗ | ✓ |
| Modular domains | ✗ | ✗ | ✗ | ✓ |
| Lightweight | ✗ | ✗ | ✗ | ✓ |

### K as a Wrapper (Optional)

Existing libraries (PyChrono, DART, Newton) can be integrated as **optional backends** only when users need advanced features beyond K's built-in capabilities:

- High-fidelity robotics simulation → use DART/PyChrono backend
- GPU-accelerated ML training → use Newton backend

But they are **not required** — K works standalone with its own implementations.

---

## 1. Project Architecture

```
K/
├── k/                          # Main package
│   ├── __init__.py             # Public API
│   ├── core/                   # Core abstractions
│   │   ├── __init__.py
│   │   ├── space.py            # Space (2D/3D) abstraction
│   │   ├── object.py           # Base physical object
│   │   ├── subsystem.py        # Group of objects
│   │   ├── state.py            # Physical state (position, velocity, temp, etc.)
│   │   └── plugin.py           # Plugin system for extensibility
│   │
│   ├── physics/                # Physics domains
│   │   ├── __init__.py
│   │   ├── mechanics/          # Classical mechanics
│   │   │   ├── __init__.py
│   │   │   ├── rigid_body.py   # Rigid body dynamics
│   │   │   ├── force.py        # Force application
│   │   │   ├── torque.py       # Torque application
│   │   │   ├── collision.py    # Collision detection/resolution
│   │   │   └── particle.py     # Particle system
│   │   │
│   │   ├── thermodynamics/     # Thermal physics
│   │   │   ├── __init__.py
│   │   │   ├── heat_transfer.py
│   │   │   ├── temperature.py
│   │   │   └── thermal_object.py
│   │   │
│   │   ├── electromagnetism/   # EM fields
│   │   │   ├── __init__.py
│   │   │   ├── electric.py
│   │   │   ├── magnetic.py
│   │   │   └── em_source.py
│   │   │
│   │   ├── optics/             # Light/optics
│   │   │   ├── __init__.py
│   │   │   ├── ray.py          # Ray tracing
│   │   │   ├── lens.py         # Lenses, mirrors
│   │   │   └── light_source.py
│   │   │
│   │   └── fluid/              # Fluid dynamics (basic)
│   │       ├── __init__.py
│   │       └── fluid_system.py
│   │
│   ├── solver/                 # Simulation engine
│   │   ├── __init__.py
│   │   ├── integrator.py       # Time integration (Euler, RK4, etc.)
│   │   ├── solver.py           # Main solver
│   │   └── scheduler.py        # Step scheduling
│   │
│   ├── calc/                   # Calculation utilities
│   │   ├── __init__.py
│   │   ├── motion.py           # Kinematics/dynamics calcs
│   │   ├── energy.py           # Energy calculations
│   │   ├── fields.py           # Field calculations
│   │   └── helpers.py          # Math helpers
│   │
│   ├── viz/                    # Visualization
│   │   ├── __init__.py
│   │   ├── base.py             # Base renderer
│   │   ├──2d.py                # 2D visualization (Matplotlib)
│   │   ├──3d.py                # 3D visualization
│   │   ├── animation.py        # Video generation
│   │   └── diagrams/           # Specialized diagrams
│   │       ├── __init__.py
│   │       ├── force_diagram.py
│   │       └── optical.py
│   │
│   └── utils/                  # Utilities
│       ├── __init__.py
│       ├── constants.py        # Physical constants
│       ├── units.py            # Unit handling
│       └── io.py               # Import/export
│
├── dev/                        # Development
│   └── plans/
│
├── tests/                     # Test suite
│
└── docs/                      # Documentation
```

### Architecture Rationale

- **Core-first**: Abstract base classes in `core/` define the contract
- **Physics as plugins**: Each domain (`mechanics`, `thermodynamics`, etc.) is a separate module that can be included/excluded
- **Solver-agnostic**: The solver works with any physics module via the state interface
- **Visualization decoupled**: Multiple backends (2D/3D) can be swapped
- **Build on existing libs**: Integrate FOSS libraries for complex domains (see Section 5)
- **Build from scratch**: Simple calculations (forces, energy, etc.) implemented directly for full control

---

## 2. Tech Stack

| Component | Primary Choice | Alternative | Notes |
|-----------|---------------|-------------|-------|
| **Core computation** | NumPy | JAX | NumPy for stability; JAX for JIT/speed |
| **Scientific computing** | SciPy | - | Optimization, interpolation, ODEs |
| **3D visualization** | PyVista | Mayavi | PyVista is more actively maintained |
| **2D visualization** | Matplotlib | - | Standard, well-documented |
| **Animation/video** | Manim | Matplotlib animation | Manim for quality videos |
| **Geometry (2D)** | Shapely | - | Mature, stable |
| **Geometry (3D)** | trimesh | PyMeshLab | trimesh is pure Python |
| **Documentation** | Sphinx | - | Standard for Python |
| **Testing** | pytest | - | Industry standard |
| **CLI (optional)** | Click | Typer | Simpler, more lightweight |

### Recommended Stack

**Core (minimal)**: `NumPy + SciPy + Matplotlib`
- Covers: calculation, basic 2D viz, ODE solving

**3D visualization**: `PyVista`
- Better maintained than Mayavi
- Works with NumPy natively
- Good for interactive + static renders

**Animation**: `Manim` (if high-quality videos needed) or `Matplotlib`
- Manim adds expressive animations (like 3Blue1Brown)
- Matplotlib for simple GIFs

---

## 3. Dependencies

### 3.1 Core Dependencies (Required)

```
k/
├── numpy
│   └── vectorized computation, array operations
├── scipy
│   ├── integrate          # ODE solvers (RK45, etc.)
│   ├── interpolate       # interpolation
│   ├── optimize          # root finding, minimization
│   └── spatial           # spatial algorithms
└── python >= 3.10
    └── type hints, structural pattern matching
```

### 3.2 Visualization Dependencies (Required for viz)

```
k/viz/
├── matplotlib
│   └── 2D plotting, basic 3D
├── pyvista
│   └── 3D rendering, VTK wrapper
└── pillow
    └── image processing, export
```

### 3.3 Optional Dependencies

```
k/viz/animation/
├── manim
│   └── high-quality video generation

k/calc/
├── numba
│   └── JIT compilation for performance

k/io/
├── h5py
│   └── HDF5 for large data export

k/geometry/
├── shapely
│   └── 2D geometry operations
└── trimesh
    └── 3D mesh operations
```

### 3.4 Development Dependencies

```
dev/
├── pytest
│   └── testing framework
├── pytest-cov
│   └── coverage reporting
├── sphinx
│   └── documentation
├── sphinx-rtd-theme
│   └── ReadTheDocs theme
├── pre-commit
│   └── git hooks
└── black
│   └── code formatting
```

---

## 4. Module Design Principles

1. **Single responsibility**: Each function does one thing
2. **Explicit inputs/outputs**: Type hints on all public functions
3. **Composition over inheritance**: Prefer function composition for flexibility
4. **Plugin architecture**: Physics domains as pluggable modules
5. **Lazy imports**: Heavy dependencies (viz) imported only when needed

### Example: Force Application

```python
# k/physics/mechanics/force.py
from numpy.typing import NDArray
from k.core.object import PhysicalObject

def apply_force(obj: PhysicalObject, force: NDArray, point: NDArray) -> None:
    """Apply a force vector to an object at a specific point."""
    obj.state.forces.append((force, point))

def net_force(forces: list[tuple[NDArray, NDArray]]) -> NDArray:
    """Calculate net force from list of (force, point) tuples."""
    return sum(f for f, _ in forces)
```

This follows the principles:
- Single responsibility: `apply_force` applies, `net_force` calculates
- Reusable: `net_force` used in subsystems, diagrams, etc.
- Extensible: User can write custom force types via plugin system

---

## 5. Reusable FOSS Physics Libraries

Instead of rewriting from scratch, integrate these existing libraries:

### 5.1 Mechanics

| Library | License | Use Case | Python-only |
|---------|---------|----------|-------------|
| **PyDy** | BSD-3 | Symbolic equation generation, multibody dynamics | Yes (SymPy-based) |
| **RBDyn** | BSD-2 | Rigid body dynamics (Featherstone algorithms) | No (C++ with bindings) |
| **Pymunk** | MIT | 2D physics (Chipmunk2D wrapper) | No (C extension) |
| **DART** | BSD-2 | Articulated body dynamics, robotics | No (C++ with dartpy) |
| **PyChrono** | BSD-3 | Full multibody simulation | No (C++ wrapper) |

**Recommendation**: 
- **2D**: Integrate **Pymunk** - simple, pythonic, well-documented
- **3D**: Integrate **PyDy** for symbolic + numerical, or **RBDyn** for pure dynamics

### 5.2 Thermodynamics

| Library | License | Use Case |
|---------|---------|----------|
| **CoolProp** | MIT | Thermophysical properties (water, air, refrigerants) |
| **Cantera** | BSD | Chemical kinetics, combustion, thermodynamics |
| **Thermo** (ChEDL) | MIT | Phase equilibria, process engineering |

**Recommendation**: **CoolProp** - lightweight, pure C with Python bindings, covers most common substances

### 5.3 Collision Detection

| Library | License | Use Case |
|---------|---------|----------|
| **PyBullet** | zlib | 3D collision, game physics |
| **fcl** | BSD | Fast collision library (C++) |
| **SDF** | MIT | Signed distance functions for collision |

**Recommendation**: **fcl** via `python-fcl` for 3D, or use Pymunk's collision if already using it

### 5.4 Updated Dependencies

```
k/physics/mechanics/
├── pymunk                 # 2D dynamics (optional)
├── pydy                   # Symbolic + numerical multibody (optional)
└── rbdl + python-rbdl     # 3D rigid body (optional)

k/physics/thermodynamics/
└── coolprop               # Thermophysical properties (optional)
```

---

## 6. Core API Design

### 6.1 Core Objects API

```python
import k

# Create space (2D or 3D)
space = k.Space(dimensions=3)  # or dimensions=2

# Create physics object
box = k.Object(shape="box", dimensions=[1, 1, 1], mass=2.0, position=[0, 0, 0])
space.add(box)

# Create physical influences
force = k.Force(vector=[0, 0, -9.8], point=[0, 0, 0])  # gravity
torque = k.Torque(vector=[0, 0, 1])
heat_source = k.HeatSource(temperature=100, location=[0, 0, 0], power=50)
light_source = k.LightSource(position=[0, 0, 10], intensity=1.0)

# Attach to object or space
box.apply(force)
box.apply(torque)
space.add(heat_source)
space.add(light_source)

# Subsystem: group of objects
subsystem = k.Subsystem(name="my_system")
subsystem.add(box)
subsystem.add(another_object)
```

### 6.2 State Model

Each `PhysicalObject` tracks these properties:

```python
@dataclass
class State:
    # Kinematics
    position: NDArray[np.float64]      # [x, y, z]
    velocity: NDArray[np.float64]       # [vx, vy, vz]
    acceleration: NDArray[np.float64]  # [ax, ay, az]
    orientation: NDArray[np.float64]    # quaternion [w, x, y, z]
    angular_velocity: NDArray[np.float64]  # [wx, wy, wz]
    
    # Dynamics
    mass: float
    inertia: NDArray[np.float64]        # 3x3 inertia tensor
    
    # Thermodynamics
    temperature: float = 298.15        # Kelvin
    heat_capacity: float = 1.0         # J/kg·K
    thermal_conductivity: float = 0.0   # W/m·K
    
    # EM (if enabled)
    charge: float = 0.0                 # Coulombs
    current: NDArray[np.float64] = None  # [Ix, Iy, Iz]
    magnetic_moment: NDArray[np.float64] = None
    
    # Applied influences
    forces: list[tuple[NDArray, NDArray]] = field(default_factory=list)  # [(force, point), ...]
    torques: list[NDArray] = field(default_factory=list)
    heat_flows: list[tuple[float, NDArray]] = field(default_factory=list)  # [(rate, location), ...]
    
    # Domain flags (what physics applies to this object)
    enabled_domains: set[str] = field(default_factory=lambda: {"mechanics"})
```

### 6.3 Plugin Contract (Physics Domains)

```python
from typing import Protocol

class PhysicsPlugin(Protocol):
    """Interface for physics domain plugins."""
    
    name: str  # e.g., "mechanics", "thermodynamics"
    version: str
    
    def initialize(self, space: "k.Space") -> None:
        """Called when domain is enabled for a space."""
        ...
    
    def compute_accelerations(self, objects: list["k.Object"], dt: float) -> None:
        """Compute accelerations for all objects."""
        ...
    
    def step(self, space: "k.Space", dt: float) -> None:
        """Advance physics by one time step."""
        ...

# Example: Thermodynamics plugin
class ThermodynamicsPlugin:
    name = "thermodynamics"
    version = "1.0.0"
    
    def initialize(self, space: k.Space) -> None:
        self.space = space
    
    def step(self, space: k.Space, dt: float) -> None:
        for obj in space.objects:
            if "thermodynamics" in obj.state.enabled_domains:
                self.update_temperature(obj, dt)
```

---

## 7. Modular Domain Selection

Users enable only the physics domains they need:

```python
# Method 1: At space creation
space = k.Space(dimensions=3, domains=["mechanics", "thermodynamics"])

# Method 2: Enable/disable at runtime
space.enable_domain("optics")
space.disable_domain("electromagnetism")
```

---

## 8. Extension Points

Users can extend K by:

1. **Custom physics modules**: Implement `PhysicsPlugin` interface
2. **Custom objects**: Extend `PhysicalObject` base class
3. **Custom integrators**: Implement `Integrator` protocol
4. **Custom renderers**: Extend `Renderer` base class
5. **Hooks**: Register callbacks for simulation events
