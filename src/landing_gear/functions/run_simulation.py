# -----------------------------
# 5. Run the simulation
# -----------------------------

from typing import Any, Dict


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
