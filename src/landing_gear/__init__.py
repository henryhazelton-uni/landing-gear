# from dataclasses import dataclass
# from enum import Enum, auto
# from typing import List, Tuple, Dict, Any
import random

from landing_gear.functions.run_simulation import print_simulation_result
from landing_gear.functions.simulation_logic import simulate_landing_gear_extension
from landing_gear.configurations.example_configurations import config_a, config_b

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
