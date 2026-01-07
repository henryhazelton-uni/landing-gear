# -----------------------------
# 1. Simple landing gear states
# -----------------------------

from enum import Enum, auto


class GearState(Enum):
    UP_LOCKED = auto()
    TRANSITIONING_DOWN = auto()
    DOWN_LOCKED = auto()
    FAILURE_DETECTED = auto()
