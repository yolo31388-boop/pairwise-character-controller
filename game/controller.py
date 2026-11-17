"""Character controller helpers (starter code with known defects)."""

import math


def integrate_velocity(vx, vy, ax, ay, dt, friction=0.0, max_speed=10.0):
    return vx, vy


def is_walkable(normal, max_slope_deg=46.0):
    return True


def project_velocity(vx, vy, nx, ny):
    return vx, vy


def step_up_allowed(rise, max_step=0.3):
    return True


def resolve_penetration(x, y, nx, ny, depth):
    return x, y


def substep_count(distance, max_step=0.02):
    return 10


def apply_gravity(vy, gravity, dt, max_fall=20.0):
    return vy


def can_coyote_jump(last_grounded_time, now, grace=0.12):
    return True


def land(vy, restitution=0.0):
    return vy

