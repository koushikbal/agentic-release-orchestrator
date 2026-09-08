from typing import Any, Dict
from pydantic import BaseModel, Field


class ReleaseState(BaseModel):
    repo_name: str = ""
    commit_hash: str = ""
    pr_diff: str = ""
    ticket_context: str = ""
    risk_score: int = Field(default=0, ge=0, le=10)
    risk_reasoning: str = ""
    deployment_approved: bool = False
    telemetry_data: Dict[str, Any] = Field(default_factory=dict)
    is_healthy: bool = False
    rollback_triggered: bool = False

