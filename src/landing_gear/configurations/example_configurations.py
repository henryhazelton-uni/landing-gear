# -----------------------------
# 4. Example configurations
# -----------------------------

from landing_gear.configurations.configuration_parameters import GearConfiguration

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
