from src.nodes.risk_analyzer import analyze_risk
from src.state import ReleaseState


def test_routine_change_gets_low_risk_without_llm(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    state = ReleaseState(pr_diff="Update copy", ticket_context="Routine documentation change")
    result = analyze_risk(state)
    assert 1 <= result["risk_score"] <= 7
    assert result["risk_reasoning"]

