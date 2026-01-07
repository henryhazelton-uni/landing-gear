from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Tuple, Dict, Any
import random


# -----------------------------
# 1. Simple landing gear states
# -----------------------------


class GearState(Enum):
    UP_LOCKED = auto()
    TRANSITIONING_DOWN = auto()
    DOWN_LOCKED = auto()
    FAILURE_DETECTED = auto()


# -----------------------------
# 2. Configuration parameters
# -----------------------------


@dataclass
class GearConfiguration:
    name: str
    pump_latency_ms: int  # Time for hydraulic pump to spin up
    actuator_speed_mm_per_100ms: float  # Extension speed
    extension_distance_mm: int  # How far the actuator must travel
    lock_time_ms: int  # Time from "down" to "locked" sensor
    requirement_time_ms: int = 8000  # Requirement: must lock within 8 seconds


# -----------------------------
# 3. Simulation logic
# -----------------------------


def simulate_landing_gear_extension(
    config: GearConfiguration, random_variation_ms: int = 0, sensor_noise_ms: int = 0
) -> Dict[str, Any]:
    """
    Simulate a landing-gear extension sequence for a given configuration.
    This is a conceptual simulation – no physics, just simple timing arithmetic.
    """
    timeline: List[Tuple[int, str, GearState]] = []

    # Start in UP_LOCKED
    current_state = GearState.UP_LOCKED
    time_ms = 0
    timeline.append((time_ms, "Initial state: gear up and locked", current_state))

    # Command issued: handle moved to DOWN
    # (no time cost for the pilot move in this simple model)
    timeline.append((time_ms, "Command issued: GEAR DOWN", current_state))

    # Pump spin-up
    pump_delay = config.pump_latency_ms + random.randint(
        -random_variation_ms, random_variation_ms
    )
    pump_delay = max(pump_delay, 0)  # don't allow negative
    time_ms += pump_delay
    current_state = GearState.TRANSITIONING_DOWN
    timeline.append(
        (time_ms, f"Hydraulic pump ready after {pump_delay} ms", current_state)
    )

    # Actuator extension
    # Convert speed in mm per 100ms to mm per ms
    speed_mm_per_ms = config.actuator_speed_mm_per_100ms / 100.0
    # Time needed = distance / speed
    if speed_mm_per_ms <= 0:
        raise ValueError("Actuator speed must be positive")

    ideal_extension_time = config.extension_distance_mm / speed_mm_per_ms

    # Add optional random variation (e.g. due to load, temperature)
    extension_time = int(ideal_extension_time) + random.randint(
        -random_variation_ms, random_variation_ms
    )
    extension_time = max(extension_time, 0)

    time_ms += extension_time
    timeline.append(
        (
            time_ms,
            f"Actuator finished extending after {extension_time} ms",
            current_state,
        )
    )

    # Sensor detection (with optional noise)
    sensor_delay = sensor_noise_ms
    time_ms += sensor_delay
    timeline.append(
        (
            time_ms,
            f"Down-position sensor triggered (+{sensor_delay} ms noise)",
            current_state,
        )
    )

    # Lock engagement
    lock_delay = config.lock_time_ms + random.randint(
        -random_variation_ms, random_variation_ms
    )
    lock_delay = max(lock_delay, 0)
    time_ms += lock_delay
    current_state = GearState.DOWN_LOCKED
    timeline.append(
        (time_ms, f"Gear locked DOWN after additional {lock_delay} ms", current_state)
    )

    total_time_ms = time_ms

    # Requirement check
    meets_requirement = total_time_ms <= config.requirement_time_ms

    # Simple failure detection: if requirement not met, mark as failure state at requirement boundary
    failure_state_time = None
    if not meets_requirement:
        failure_state_time = config.requirement_time_ms
        timeline.append(
            (
                failure_state_time,
                f"Requirement breached (> {config.requirement_time_ms} ms). System would flag failure.",
                GearState.FAILURE_DETECTED,
            )
        )

    return {
        "config": config,
        "timeline": timeline,
        "total_time_ms": total_time_ms,
        "meets_requirement": meets_requirement,
        "failure_state_time": failure_state_time,
    }


# -----------------------------
# 4. Example configurations
# -----------------------------

# Configuration A: shared hydraulic pump (slower)
config_a = GearConfiguration(
    name="Config A – Shared Pump",
    pump_latency_ms=300,  # slower pump spin-up
    actuator_speed_mm_per_100ms=8.0,  # slower actuator
    extension_distance_mm=700,  # mm to travel
    lock_time_ms=300,  # lock engagement time
    requirement_time_ms=8000,  # 8 seconds requirement
)

# Configuration B: dedicated pump (faster)
config_b = GearConfiguration(
    name="Config B – Dedicated Pump",
    pump_latency_ms=100,  # quicker pump spin-up
    actuator_speed_mm_per_100ms=12.0,  # faster actuator
    extension_distance_mm=700,
    lock_time_ms=300,
    requirement_time_ms=8000,
)


# -----------------------------
# 5. Run the simulation
# -----------------------------


def print_simulation_result(result: Dict[str, Any]) -> None:
    config = result["config"]
    print("=" * 70)
    print(f"Simulation for {config.name}")
    print("=" * 70)
    for t, msg, state in result["timeline"]:
        print(f"[t = {t:5d} ms]  {state.name:18s}  - {msg}")

    print("\nSummary:")
    print(
        f"  Total time to DOWN_LOCKED: {result['total_time_ms']} ms "
        f"({result['total_time_ms'] / 1000:.2f} s)"
    )
    print(
        f"  Requirement: must lock within {config.requirement_time_ms} ms "
        f"({config.requirement_time_ms / 1000:.2f} s)"
    )

    if result["meets_requirement"]:
        print("  ✅ Requirement MET")
    else:
        print("  ❌ Requirement NOT MET – configuration would be flagged for review")
    print()


def main() -> None:
    """Entry point for the landing-gear command."""
    # Fix seed for reproducibility in teaching
    random.seed(42)

    # You can adjust variation to show different runs
    variation_ms = 200
    sensor_noise_ms = 50

    result_a = simulate_landing_gear_extension(
        config_a, random_variation_ms=variation_ms, sensor_noise_ms=sensor_noise_ms
    )
    result_b = simulate_landing_gear_extension(
        config_b, random_variation_ms=variation_ms, sensor_noise_ms=sensor_noise_ms
    )

    print_simulation_result(result_a)
    print_simulation_result(result_b)


if __name__ == "__main__":
    main()
