import pytest

from game.controller import (apply_gravity, can_coyote_jump, integrate_velocity,
                             is_walkable, land, project_velocity,
                             resolve_penetration, step_up_allowed, substep_count)


def test_integrate_applies_horizontal_acceleration():
    vx, _ = integrate_velocity(0.0, 0.0, 2.0, 0.0, 0.5)
    assert vx == pytest.approx(1.0)


def test_friction_decays_horizontal_speed():
    vx, _ = integrate_velocity(10.0, 0.0, 0.0, 0.0, 0.5, friction=1.0)
    assert vx == pytest.approx(5.0)


def test_speed_is_clamped_to_max_speed():
    vx, _ = integrate_velocity(0.0, 0.0, 10.0, 0.0, 1.0, max_speed=3.0)
    assert vx == pytest.approx(3.0)


def test_flat_ground_is_walkable():
    assert is_walkable((0.0, 1.0)) is True
    assert is_walkable((0.2, 1.0)) is True
    assert is_walkable((0.9, 0.4359)) is False


def test_steep_slope_is_not_walkable():
    assert is_walkable((0.9, 0.4359)) is False


def test_velocity_is_projected_onto_ground_plane():
    vx, vy = project_velocity(4.0, -3.0, 0.0, 1.0)
    assert vx == pytest.approx(4.0)
    assert vy == pytest.approx(0.0)


def test_small_step_up_is_allowed():
    assert step_up_allowed(0.25, max_step=0.3) is True
    assert step_up_allowed(0.0, max_step=0.3) is False


def test_tall_step_up_is_rejected():
    assert step_up_allowed(0.4, max_step=0.3) is False


def test_penetration_is_resolved_along_normal():
    x, y = resolve_penetration(0.0, 0.0, 0.0, 1.0, 0.2)
    assert y == pytest.approx(0.2)
    assert x == pytest.approx(0.0)


def test_fast_movement_uses_substeps():
    assert substep_count(1.0, max_step=0.02) == 50


def test_slow_movement_uses_one_substep():
    assert substep_count(0.01, max_step=0.02) == 1


def test_gravity_changes_vertical_velocity():
    assert apply_gravity(0.0, -10.0, 0.5) == pytest.approx(-5.0)


def test_fall_speed_is_clamped():
    assert apply_gravity(-50.0, -10.0, 1.0, max_fall=20.0) == pytest.approx(-20.0)


def test_coyote_time_allows_airborne_jump():
    assert can_coyote_jump(0.95, 1.0, grace=0.12) is True
    assert can_coyote_jump(0.95, 1.2, grace=0.12) is False


def test_landing_clears_downward_velocity():
    assert land(-8.0, restitution=0.0) == pytest.approx(0.0)


