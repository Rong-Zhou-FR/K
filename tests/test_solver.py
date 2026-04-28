import numpy as np
import pytest

from k.core.object import PhysicalObject
from k.core.plugin import PhysicsPlugin
from k.core.state import State, Wrench6T
from k.core.space import Space
from k.solver import EulerIntegrator, RK4Integrator, VerletIntegrator, Solver


class ConstantAccelPlugin:
    def __init__(self, force: np.ndarray) -> None:
        self.force = force
        self.name = "constant_accel"
        self.version = "0.1.0"

    def initialize(self, space: Space) -> None:
        pass

    def compute_accelerations(
        self, objects: list[PhysicalObject], dt: float
    ) -> None:
        for obj in objects:
            wrench = np.zeros(6, dtype=np.float64)
            wrench[:3] = self.force
            point = obj.state.position.copy()
            obj.state.wrenches.append((wrench, point))

    def step(self, space: Space, dt: float) -> None:
        pass


def make_state(pos: np.ndarray, vel: np.ndarray) -> State:
    return State(
        position=pos.astype(np.float64),
        velocity=vel.astype(np.float64),
        acceleration=np.zeros(3, dtype=np.float64),
        orientation=np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64),
        angular_velocity=np.zeros(3, dtype=np.float64),
        mass=1.0,
        inertia=np.eye(3, dtype=np.float64),
    )


def test_euler_integrator_linear_motion() -> None:
    integrator = EulerIntegrator()
    state = make_state(np.zeros(3), np.zeros(3))
    force = np.array([1.0, 0.0, 0.0])
    wrench = np.zeros(6, dtype=np.float64)
    wrench[:3] = force
    state.wrenches.append((wrench, state.position.copy()))
    state.net_wrench = wrench.copy()
    dt = 0.1
    integrator.step(state, dt)
    assert np.allclose(state.velocity, [0.1, 0.0, 0.0])
    assert np.allclose(state.position, [0.01, 0.0, 0.0])


def test_rk4_integrator_linear_motion() -> None:
    integrator = RK4Integrator()
    state = make_state(np.zeros(3), np.zeros(3))
    force = np.array([1.0, 0.0, 0.0])
    wrench = np.zeros(6, dtype=np.float64)
    wrench[:3] = force
    state.wrenches.append((wrench, state.position.copy()))
    state.net_wrench = wrench.copy()
    dt = 0.1
    integrator.step(state, dt)
    assert np.allclose(state.velocity, [0.1, 0.0, 0.0])
    assert np.allclose(state.position, [0.005, 0.0, 0.0])


def test_verlet_integrator_linear_motion() -> None:
    integrator = VerletIntegrator()
    state = make_state(np.zeros(3), np.zeros(3))
    force = np.array([1.0, 0.0, 0.0])
    wrench = np.zeros(6, dtype=np.float64)
    wrench[:3] = force
    state.wrenches.append((wrench, state.position.copy()))
    state.net_wrench = wrench.copy()
    dt = 0.1
    integrator.step(state, dt)
    assert np.allclose(state.velocity, [0.1, 0.0, 0.0])
    assert np.allclose(state.position, [0.005, 0.0, 0.0])


def test_solver_with_dummy_plugin() -> None:
    space = Space(dimensions=3)
    state = make_state(np.zeros(3), np.zeros(3))
    obj = PhysicalObject(shape="point", state=state, id="test")
    space.add(obj)
    plugin = ConstantAccelPlugin(force=np.array([1.0, 0.0, 0.0]))
    solver = Solver(space, RK4Integrator(), dt=0.01)
    solver.register_plugin(plugin)
    solver.run(duration=1.0)
    assert np.allclose(obj.state.position, [0.5, 0.0, 0.0], atol=1e-3)
    assert np.allclose(obj.state.velocity, [1.0, 0.0, 0.0], atol=1e-3)


def test_solver_invalid_dt() -> None:
    space = Space()
    with pytest.raises(ValueError):
        Solver(space, EulerIntegrator(), dt=0.0)


def test_solver_step_count() -> None:
    space = Space(dimensions=3)
    state = make_state(np.zeros(3), np.zeros(3))
    obj = PhysicalObject(shape="point", state=state, id="test")
    space.add(obj)
    plugin = ConstantAccelPlugin(force=np.array([0.0, 0.0, 0.0]))
    solver = Solver(space, EulerIntegrator(), dt=0.1)
    solver.register_plugin(plugin)
    solver.step(n=5)
    assert np.isclose(solver.time, 0.5)
