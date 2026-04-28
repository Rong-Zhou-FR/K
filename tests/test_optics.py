import numpy as np
import pytest

from k.physics.optics import (
    LightSource,
    Mirror,
    OpticalSystem,
    Ray,
    ThinLens,
    critical_angle,
    is_total_internal_reflection,
    reflect,
    refract,
    snell_angle,
)


def make_ray() -> Ray:
    return Ray(
        origin=np.array([0.0, 0.0, 0.0]),
        direction=np.array([0.0, 0.0, 1.0]),
        wavelength=550e-9,
    )


def make_ray_direction(direction: np.ndarray) -> Ray:
    return Ray(
        origin=np.array([0.0, 0.0, 0.0]),
        direction=direction,
        wavelength=550e-9,
    )


class TestRay:
    def test_ray_creation(self) -> None:
        origin = np.array([0.0, 0.0, 0.0])
        direction = np.array([0.0, 0.0, 1.0])
        ray = Ray(origin=origin.copy(), direction=direction.copy(), wavelength=550e-9)
        assert np.allclose(ray.origin, origin)
        assert ray.normalized is True

    def test_ray_auto_normalize(self) -> None:
        direction = np.array([0.0, 0.0, 2.0])
        ray = Ray(
            origin=np.zeros(3),
            direction=direction.copy(),
            wavelength=550e-9,
        )
        assert np.allclose(ray.direction, np.array([0.0, 0.0, 1.0]))
        assert ray.normalized is True

    def test_ray_at_distance(self) -> None:
        ray = make_ray()
        point = ray.at(5.0)
        assert np.allclose(point, np.array([0.0, 0.0, 5.0]))

    def test_ray_frequency(self) -> None:
        ray = make_ray()
        c = 299_792_458.0
        expected_freq = c / 550e-9
        assert np.isclose(ray.frequency, expected_freq)

    def test_ray_wave_number(self) -> None:
        ray = make_ray()
        expected_kn = 2 * np.pi / 550e-9
        assert np.isclose(ray.wave_number, expected_kn)


class TestLightSource:
    def test_light_source_creation(self) -> None:
        position = np.array([0.0, 0.0, 0.0])
        source = LightSource(
            position=position.copy(),
            intensity=1.0,
            wavelength=550e-9,
        )
        assert np.allclose(source.position, position)
        assert source.intensity == 1.0
        assert source.wavelength == 550e-9

    def test_light_source_emit_ray(self) -> None:
        source = LightSource(
            position=np.zeros(3),
            intensity=1.0,
            wavelength=550e-9,
        )
        direction = np.array([0.0, 0.0, 1.0])
        ray = source.emit_ray(direction)
        assert np.allclose(ray.origin, source.position)
        assert ray.normalized is True

    def test_light_source_frequency(self) -> None:
        source = LightSource(
            position=np.zeros(3),
            intensity=1.0,
            wavelength=550e-9,
        )
        c = 299_792_458.0
        expected_freq = c / 550e-9
        assert np.isclose(source.frequency, expected_freq)


class TestSnellLaw:
    def test_refract_perpendicular(self) -> None:
        ray = make_ray()
        normal = np.array([0.0, 0.0, -1.0])
        refracted = refract(ray=ray, normal=normal, n1=1.0, n2=1.5)
        assert refracted is not None
        assert refracted is not None

    def test_refract_at_angle(self) -> None:
        ray = Ray(
            origin=np.array([0.0, 0.0, 0.0]),
            direction=np.array([0.0, 0.70710678, 0.70710678]),
            wavelength=550e-9,
            normalized=True,
        )
        normal = np.array([0.0, 0.0, 1.0])
        refracted = refract(ray=ray, normal=normal, n1=1.0, n2=1.5)
        assert refracted is not None

    def test_refract_total_internal_reflection(self) -> None:
        ray = make_ray()
        ray.direction = np.array([0.0, 0.70710678, -0.70710678])
        ray.origin = np.array([0.0, 0.0, 1.0])
        normal = np.array([0.0, 0.0, -1.0])
        refracted = refract(ray=ray, normal=normal, n1=1.5, n2=1.0)
        assert refracted is None

    def test_reflect(self) -> None:
        ray = make_ray()
        normal = np.array([0.0, 1.0, 0.0])
        reflected = reflect(ray=ray, normal=normal)
        assert np.allclose(reflected.direction, np.array([0.0, 0.0, 1.0]))

    def test_snell_angle(self) -> None:
        theta_i = np.pi / 6
        theta_t = snell_angle(theta_i, 1.0, 1.5)
        assert theta_t is not None
        assert 0 < theta_t < np.pi / 2

    def test_critical_angle(self) -> None:
        theta_c = critical_angle(1.5, 1.0)
        assert theta_c is not None
        assert 0 < theta_c < np.pi / 2

    def test_is_total_internal_reflection(self) -> None:
        assert is_total_internal_reflection(np.pi / 3, 1.5, 1.0) == True
        assert is_total_internal_reflection(np.pi / 6, 1.5, 1.0) == False


class TestThinLens:
    def test_thin_lens_creation(self) -> None:
        lens = ThinLens(
            focal_length=1.0,
            center=np.array([0.0, 0.0, 5.0]),
            normal=np.array([0.0, 0.0, -1.0]),
            material_n=1.5,
        )
        assert lens.focal_length == 1.0
        assert lens.material_n == 1.5

    def test_thin_lens_intersect(self) -> None:
        lens = ThinLens(
            focal_length=1.0,
            center=np.array([0.0, 0.0, 5.0]),
            normal=np.array([0.0, 0.0, 1.0]),
        )
        ray = make_ray()
        t, hit = lens.intersect(ray)
        assert hit == True
        assert np.isclose(t, 5.0)

    def test_thin_lens_refract(self) -> None:
        lens = ThinLens(
            focal_length=1.0,
            center=np.array([0.0, 0.0, 5.0]),
            normal=np.array([0.0, 0.0, 1.0]),
        )
        ray = make_ray()
        refracted = lens.refract(ray)
        assert refracted is not None


class TestMirror:
    def test_mirror_creation(self) -> None:
        mirror = Mirror(
            normal=np.array([0.0, 0.0, 1.0]),
            position=np.array([0.0, 0.0, 5.0]),
        )
        assert mirror.curvature_type == "plane"

    def test_mirror_intersect(self) -> None:
        mirror = Mirror(
            normal=np.array([0.0, 0.0, -1.0]),
            position=np.array([0.0, 0.0, 5.0]),
        )
        ray = make_ray()
        t, hit = mirror.intersect(ray)
        assert hit == True

    def test_mirror_reflect(self) -> None:
        mirror = Mirror(
            normal=np.array([0.0, 0.0, -1.0]),
            position=np.array([0.0, 0.0, 5.0]),
        )
        ray = make_ray()
        reflected = mirror.reflect(ray)
        assert np.allclose(reflected.direction, np.array([0.0, 0.0, -1.0]))


class TestOpticalSystem:
    def test_empty_system_trace(self) -> None:
        system = OpticalSystem()
        ray = make_ray()
        traced = system.trace(ray)
        assert traced == []

    def test_system_with_lens(self) -> None:
        lens = ThinLens(
            focal_length=1.0,
            center=np.array([0.0, 0.0, 5.0]),
            normal=np.array([0.0, 0.0, 1.0]),
        )
        system = OpticalSystem()
        system.add(lens)
        ray = make_ray()
        traced = system.trace(ray)
        assert len(traced) > 0


class TestIntegration:
    def test_full_optical_system(self) -> None:
        source = LightSource(
            position=np.array([0.0, 0.0, 0.0]),
            intensity=1.0,
            wavelength=550e-9,
        )
        lens = ThinLens(
            focal_length=1.0,
            center=np.array([0.0, 0.0, 5.0]),
            normal=np.array([0.0, 0.0, 1.0]),
        )
        mirror = Mirror(
            normal=np.array([0.0, 0.0, -1.0]),
            position=np.array([0.0, 0.0, 10.0]),
        )
        system = OpticalSystem()
        system.add(lens)
        system.add(mirror)
        ray = source.emit_ray(np.array([0.0, 0.0, 1.0]))
        traced = system.trace(ray)
        assert len(traced) > 0