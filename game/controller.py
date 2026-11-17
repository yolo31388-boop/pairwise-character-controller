"""Character controller helpers.

Pure functions used by the character controller.  Keeping the physics math
here (instead of inside the render loop) makes the fixed-step simulation
deterministic and independently testable regardless of frame rate.
"""

import math


def integrate_velocity(vx, vy, ax, ay, dt, friction=0.0, max_speed=10.0):
    """Integrate acceleration, apply friction and clamp to ``max_speed``.

    Acceleration is integrated first (``v += a * dt``), then friction scales
    the whole velocity vector by ``1 - friction * dt`` (clamped at zero so the
    factor never reverses direction at low frame rates), and finally the
    resulting speed is clamped to ``max_speed``.
    """
    vx += ax * dt
    vy += ay * dt

    damping = max(0.0, 1.0 - friction * dt)
    vx *= damping
    vy *= damping

    speed = math.hypot(vx, vy)
    if speed > max_speed and speed > 0.0:
        scale = max_speed / speed
        vx *= scale
        vy *= scale

    return vx, vy


def is_walkable(normal, max_slope_deg=46.0):
    """Return True if a surface normal is shallow enough to stand on.

    The surface counts as walkable when the angle between its normal and the
    up axis does not exceed ``max_slope_deg``; steeper surfaces (including
    vertical walls) are rejected.
    """
    nx, ny = normal
    length = math.hypot(nx, ny)
    if length == 0.0:
        return False
    ny /= length
    return ny >= math.cos(math.radians(max_slope_deg))


def project_velocity(vx, vy, nx, ny):
    """Project a velocity onto the contact plane by removing its normal part.

    ``v' = v - (v . n) n``.  Prevents the character from pushing into a wall
    or sliding through a slope while preserving tangential movement.
    """
    length = math.hypot(nx, ny)
    if length == 0.0:
        return vx, vy
    nx /= length
    ny /= length
    normal_component = vx * nx + vy * ny
    return vx - normal_component * nx, vy - normal_component * ny


def step_up_allowed(rise, max_step=0.3):
    """Return True if a ledge of height ``rise`` may be stepped onto.

    Zero/negative rises are not steps (the contact is handled as a wall or
    flat ground), and anything taller than ``max_step`` blocks the character.
    """
    return 0.0 < rise <= max_step


def resolve_penetration(x, y, nx, ny, depth):
    """Push an embedded character out along the contact normal."""
    length = math.hypot(nx, ny)
    if length == 0.0:
        return x, y
    return x + nx / length * depth, y + ny / length * depth


def substep_count(distance, max_step=0.02):
    """Number of collision substeps needed to travel ``distance`` safely.

    Each substep may move at most ``max_step`` world units so that fast
    movement cannot tunnel through thin colliders.  Always at least one.
    """
    return max(1, math.ceil(abs(distance) / max_step))


def apply_gravity(vy, gravity, dt, max_fall=20.0):
    """Integrate gravity and clamp the downward speed to ``max_fall``."""
    return max(-max_fall, vy + gravity * dt)


def can_coyote_jump(last_grounded_time, now, grace=0.12):
    """Return True while within the coyote-time window after leaving ground.

    A jump is allowed only when the character was grounded within the last
    ``grace`` seconds; this never grants a mid-air double jump.
    """
    elapsed = now - last_grounded_time
    return 0.0 <= elapsed <= grace


def land(vy, restitution=0.0):
    """Resolve a landing: cancel (or bounce) the downward velocity.

    With ``restitution == 0`` the character sticks to the ground; positive
    restitution returns a fraction of the impact speed upward.  Upward
    velocity (e.g. after a jump) is left untouched.
    """
    if vy < 0.0:
        return -vy * restitution
    return vy
