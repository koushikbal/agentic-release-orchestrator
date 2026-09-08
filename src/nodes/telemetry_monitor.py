import requests
from src.config import get_settings
from src.state import ReleaseState


def monitor_telemetry(state: ReleaseState) -> dict:
    settings = get_settings()
    response = requests.get(settings.telemetry_url, timeout=settings.metrics_timeout_seconds)
    response.raise_for_status()
    return {"telemetry_data": response.json()}

