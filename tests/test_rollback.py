from src.graph import release_graph
from src.state import ReleaseState


def test_high_risk_release_halts_before_telemetry(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    result = release_graph.invoke(ReleaseState(pr_diff="breaking database migration", ticket_context="security auth migration"))
    assert result["deployment_approved"] is False
    assert result["rollback_triggered"] is False


def test_healthy_approved_release_does_not_rollback(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr("src.nodes.telemetry_monitor.requests.get", lambda *a, **k: type("R", (), {"raise_for_status": lambda self: None, "json": lambda self: {"error_rate_percent": 0.1, "latency_ms": 100}})())
    result = release_graph.invoke(ReleaseState(pr_diff="Update copy", ticket_context="Routine change"))
    assert result["deployment_approved"] is True
    assert result["is_healthy"] is True
    assert result["rollback_triggered"] is False


def test_unhealthy_release_requires_rollback_configuration(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    monkeypatch.setattr("src.nodes.telemetry_monitor.requests.get", lambda *a, **k: type("R", (), {"raise_for_status": lambda self: None, "json": lambda self: {"error_rate_percent": 4.0, "latency_ms": 700}})())
    try:
        release_graph.invoke(ReleaseState(pr_diff="Update copy", ticket_context="Routine change"))
    except RuntimeError as exc:
        assert "GITHUB_TOKEN" in str(exc)
    else:
        raise AssertionError("Unhealthy telemetry must fail closed when rollback is not configured")
