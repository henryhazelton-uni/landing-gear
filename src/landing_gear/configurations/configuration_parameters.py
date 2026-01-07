# -----------------------------
# 2. Configuration parameters
# -----------------------------


from dataclasses import dataclass


@dataclass
class GearConfiguration:
    name: str
    pump_latency_ms: int  # Time for hydraulic pump to spin up
    actuator_speed_mm_per_100ms: float  # Extension speed
    extension_distance_mm: int  # How far the actuator must travel
    lock_time_ms: int  # Time from "down" to "locked" sensor
    requirement_time_ms: int = 8000  # Requirement: must lock within 8 seconds
