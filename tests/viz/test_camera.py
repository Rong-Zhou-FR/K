from __future__ import annotations

from k.viz.camera import CameraAngle, CameraPreset
import numpy as np


def test_camera_angle_defaults() -> None:
    pos = np.array([10, 0, 0], dtype=np.float64)
    cam = CameraAngle(position=pos)
    assert np.allclose(cam.position, pos)
    assert np.allclose(cam.focal_point, np.array([0, 0, 0], dtype=np.float64))
    assert np.allclose(cam.view_up, np.array([0, 0, 1], dtype=np.float64))


def test_camera_angle_custom() -> None:
    pos = np.array([1, 2, 3], dtype=np.float64)
    focal = np.array([4, 5, 6], dtype=np.float64)
    up = np.array([0, 1, 0], dtype=np.float64)
    cam = CameraAngle(position=pos, focal_point=focal, view_up=up)
    assert np.allclose(cam.position, pos)
    assert np.allclose(cam.focal_point, focal)
    assert np.allclose(cam.view_up, up)


def test_camera_preset_top() -> None:
    cam = CameraPreset.top()
    assert np.allclose(cam.position, np.array([0, 0, 10], dtype=np.float64))


def test_camera_preset_front() -> None:
    cam = CameraPreset.front()
    assert np.allclose(cam.position, np.array([10, 0, 0], dtype=np.float64))


def test_camera_preset_side() -> None:
    cam = CameraPreset.side()
    assert np.allclose(cam.position, np.array([0, 10, 0], dtype=np.float64))


def test_camera_preset_isometric() -> None:
    cam = CameraPreset.isometric()
    assert np.allclose(cam.position, np.array([8, 8, 8], dtype=np.float64))
