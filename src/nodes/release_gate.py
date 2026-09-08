from src.state import ReleaseState


def evaluate_release_gate(state: ReleaseState) -> dict:
    return {"deployment_approved": 1 <= state.risk_score <= 7}

