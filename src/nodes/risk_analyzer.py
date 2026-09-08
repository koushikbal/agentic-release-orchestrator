import json
from typing import Any
from src.config import get_settings
from src.state import ReleaseState


def _heuristic(diff: str, ticket: str) -> tuple[int, str]:
    text = f"{diff} {ticket}".lower()
    indicators = {"database": 3, "migration": 3, "auth": 2, "security": 2, "rollback": 1, "breaking": 3}
    score = min(10, max(1, 3 + sum(value for word, value in indicators.items() if word in text)))
    return score, "Heuristic assessment: " + ("elevated change indicators detected." if score > 3 else "routine change profile.")


def analyze_risk(state: ReleaseState) -> dict:
    """Analyze release context with OpenAI when configured, otherwise safely degrade locally."""
    settings = get_settings()
    if not settings.openai_api_key:
        score, reasoning = _heuristic(state.pr_diff, state.ticket_context)
        return {"risk_score": score, "risk_reasoning": reasoning}
    from openai import OpenAI
    client = OpenAI(api_key=settings.openai_api_key)
    response = client.chat.completions.create(
        model=settings.openai_model,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Return only JSON with integer risk_score 1-10 and concise risk_reasoning."},
            {"role": "user", "content": json.dumps({"diff": state.pr_diff, "ticket": state.ticket_context})},
        ],
    )
    payload: dict[str, Any] = json.loads(response.choices[0].message.content or "{}")
    score = min(10, max(1, int(payload.get("risk_score", 10))))
    return {"risk_score": score, "risk_reasoning": str(payload.get("risk_reasoning", "No reasoning returned."))}

