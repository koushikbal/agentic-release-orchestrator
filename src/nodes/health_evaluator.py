from src.state import ReleaseState


def evaluate_health(state: ReleaseState) -> dict:
    metrics = state.telemetry_data
    error_rate = float(metrics.get("error_rate_percent", metrics.get("error_rate", 100)))
    latency = float(metrics.get("latency_ms", 10000))
    return {"is_healthy": error_rate <= 2.0 and latency <= 500.0}

