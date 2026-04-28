import numpy as np
import pytest

from k.core.object import PhysicalObject
from k.core.state import State, Wrench6T
from k.physics.mechanics import (
    CollisionBox,
    CollisionCapsule,
    CollisionSphere,
    Force,
    MechanicsPlugin,
    Particle,
    RigidBody,
    Torque,
    apply_force,
    apply_torque,
    net_force,
    net_torque,
)
from k.solver import RK4Integrator, Solver
from k.core.space import Space


def make_state(pos=None, vel=None):
    if pos is None:
        pos = np.zeros(3, dtype=np.float64)
    if vel is None:
        vel = np.zeros(3, dtype=np.float64)
    return State(
        position=pos.astype(np.float64),
        velocity=vel.astype(np.float64),
        acceleration=np.zeros(3, dtype=np.float64),
        orientation=np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64),
        angular_velocity=np.zeros(3, dtype=np.float64),
        mass=1.0,
        inertia=np.eye(3, dtype=np.float64),
    )


class TestForce:
    def test_force_creation(self) -> None:
        f = Force(force=np.array([1.0, 0.0, 0.0]), point=np.zeros(3))
        assert np.all(f.force == [1.0, 0.0, 0.0])

    def test_force_to_wrench(self) -> None:
        f = Force(force=np.array([1.0, 2.0, 3.0]), point=np.zeros(3))
        w = f.to_wrench()
        assert np.all(w[:3] == [1.0, 2.0, 3.0])
        assert np.all(w[3:] == 0.0)


class TestTorque:
    def test_torque_creation(self) -> None:
        t = Torque(torque=np.array([0.0, 0.0, 1.0]))
        assert t.torque[2] == 1.0

    def test_torque_to_wrench(self) -> None:
        t = Torque(torque=np.array([1.0, 2.0, 3.0]))
        w = t.to_wrench()
        assert np.all(w[:3] == 0.0)
        assert np.all(w[3:] == [1.0, 2.0, 3.0])


class TestParticle:
    def test_particle_creation(self) -> None:
        state = make_state()
        p = Particle(shape="point", state=state)
        assert p.shape == "point"

    def test_particle_inherits_physical_object(self) -> None:
        from k.core.object import PhysicalObject

        state = make_state()
        p = Particle(shape="point", state=state)
        assert isinstance(p, PhysicalObject)


class TestRigidBody:
    def test_rigid_body_creation(self) -> None:
        state = make_state()
        rb = RigidBody(shape="box", state=state)
        assert rb.shape == "box"

    def test_rigid_body_with_sphere(self) -> None:
        state = make_state()
        sphere = CollisionSphere(radius=1.0)
        rb = RigidBody(shape="sphere", state=state, collision_shape=sphere)
        assert isinstance(rb.collision_shape, CollisionSphere)

    def test_rigid_body_with_box(self) -> None:
        state = make_state()
        box = CollisionBox(half_extents=np.array([1.0, 1.0, 1.0]))
        rb = RigidBody(shape="box", state=state, collision_shape=box)
        assert isinstance(rb.collision_shape, CollisionBox)

    def test_rigid_body_with_capsule(self) -> None:
        state = make_state()
        cap = CollisionCapsule(radius=0.5, half_height=2.0)
        rb = RigidBody(shape="capsule", state=state, collision_shape=cap)
        assert isinstance(rb.collision_shape, CollisionCapsule)


class TestApplyFunctions:
    def test_apply_force(self) -> None:
        state = make_state()
        obj = Particle(shape="point", state=state)
        f = Force(force=np.array([1.0, 0.0, 0.0]), point=np.zeros(3))
        apply_force(obj, f)
        assert len(obj.state.wrenches) == 1
        assert np.all(obj.state.wrenches[0][0][:3] == [1.0, 0.0, 0.0])

    def test_apply_torque(self) -> None:
        state = make_state()
        obj = RigidBody(shape="box", state=state)
        t = Torque(torque=np.array([0.0, 0.0, 1.0]))
        apply_torque(obj, t)
        assert len(obj.state.wrenches) == 1
        assert np.all(obj.state.wrenches[0][0][3:] == [0.0, 0.0, 1.0])


class TestNetCalculations:
    def test_net_force(self) -> None:
        state = make_state()
        obj = Particle(shape="point", state=state)
        f1 = Force(force=np.array([1.0, 0.0, 0.0]), point=np.zeros(3))
        f2 = Force(force=np.array([0.0, 1.0, 0.0]), point=np.zeros(3))
        apply_force(obj, f1)
        apply_force(obj, f2)
        nf = net_force(obj.state.wrenches)
        assert np.all(nf == [1.0, 1.0, 0.0])

    def test_net_torque(self) -> None:
        state = make_state()
        obj = RigidBody(shape="box", state=state)
        t1 = Torque(torque=np.array([0.0, 0.0, 1.0]))
        t2 = Torque(torque=np.array([0.0, 1.0, 0.0]))
        apply_torque(obj, t1)
        apply_torque(obj, t2)
        nt = net_torque(obj.state.wrenches, state)
        assert np.all(nt == [0.0, 1.0, 1.0])


class TestMechanicsPlugin:
    def test_plugin_initialization(self) -> None:
        space = Space(dimensions=3)
        plugin = MechanicsPlugin()
        plugin.initialize(space)
        assert "mechanics" in space.enabled_domains

    def test_plugin_compute_accelerations(self) -> None:
        state = make_state()
        obj = Particle(shape="point", state=state, id="test")
        space = Space(dimensions=3)
        space.add(obj)
        plugin = MechanicsPlugin()
        plugin.initialize(space)
        f = Force(force=np.array([1.0, 0.0, 0.0]), point=np.zeros(3))
        apply_force(obj, f)
        plugin.compute_accelerations([obj], 0.01)
        assert np.all(obj.state.net_wrench[:3] == [1.0, 0.0, 0.0])

    def test_plugin_with_solver(self) -> None:
        state = make_state()
        obj = Particle(shape="point", state=state, id="test")
        space = Space(dimensions=3)
        space.add(obj)
        plugin = ConstantForcePlugin(force=np.array([1.0, 0.0, 0.0]))
        solver = Solver(space, RK4Integrator(), dt=0.01)
        solver.register_plugin(plugin)
        solver.run(duration=1.0)
        assert np.allclose(obj.state.position[0], 0.5, atol=1e-2)


class ConstantForcePlugin:
    def __init__(self, force: np.ndarray) -> None:
        self.force = force
        self.name = "constant_force"
        self.version = "0.1.0"

    def initialize(self, space: Space) -> None:
        pass

    def compute_accelerations(
        self, objects: list[PhysicalObject], dt: float
    ) -> None:
        for obj in objects:
            f = Force(force=self.force, point=obj.state.position.copy())
            apply_force(obj, f)

    def step(self, space: Space, dt: float) -> None:
        pass
