# -----------------------------
# 3. Simulation logic
# -----------------------------

import random
import time
from typing import List, Tuple, Dict, Any
from landing_gear.configurations.configuration_parameters import GearConfiguration
from landing_gear.configurations.gear_states import GearState
from landing_gear.functions.progress_bar import progress_bar


def simulate_landing_gear_extension(
    config: GearConfiguration, random_variation_ms: int = 0, sensor_noise_ms: int = 0
) -> Dict[str, Any]:
    """
    Simulate a landing-gear extension sequence for a given configuration.
    This is a conceptual simulation – no physics, just simple timing arithmetic.
    """
    # Once all the delays are initated, the time taken can be used to be the condition of a while loop for progress bar

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

    # Sensor detection (with optional noise)
    sensor_delay = sensor_noise_ms

    # Lock engagement
    lock_delay = config.lock_time_ms + random.randint(
        -random_variation_ms, random_variation_ms
    )
    lock_delay = max(lock_delay, 0)

    # Gather all the time_ms appended things
    time_ms += pump_delay
    current_state = GearState.TRANSITIONING_DOWN
    timeline.append(
        (time_ms, f"Hydraulic pump ready after {pump_delay} ms", current_state)
    )

    time_ms += extension_time
    timeline.append(
        (
            time_ms,
            f"Actuator finished extending after {extension_time} ms",
            current_state,
        )
    )

    time_ms += sensor_delay
    timeline.append(
        (
            time_ms,
            f"Down-position sensor triggered (+{sensor_delay} ms noise)",
            current_state,
        )
    )

    time_ms += lock_delay
    current_state = GearState.DOWN_LOCKED
    timeline.append(
        (time_ms, f"Gear locked DOWN after additional {lock_delay} ms", current_state)
    )

    total_delay_time_ms = pump_delay + extension_time + sensor_delay + lock_delay

    # Add a progress bar
    steps = 100
    counter = 0
    sleep_per_step = (
        total_delay_time_ms / steps / 1000
    )  # Converting ms to seconds to make progress bar more even
    print("Starting extension of landing gear:")
    start_time = time.time()
    while counter < steps + 1:
        progress_bar(
            counter,
            steps,
            prefix="Extending Landing Gear: ",
            suffix="Landing Gear Extended",
            fill="#",
        )
        time.sleep(sleep_per_step)
        counter += 1
    end_time = time.time()
    time_taken = end_time - start_time
    print()
    print(f"Time taken to execute: {time_taken:.2f} seconds")
    print()

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
