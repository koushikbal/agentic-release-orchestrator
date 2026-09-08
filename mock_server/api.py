import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Release Orchestrator Mock APIs", version="1.0.0")
healthy = os.getenv("MOCK_HEALTHY", "true").lower() == "true"


class DeployRequest(BaseModel):
    repo_name: str
    commit_hash: str


@app.post("/deploy")
def deploy(request: DeployRequest):
    return {"accepted": True, "repo_name": request.repo_name, "commit_hash": request.commit_hash, "status": "synced"}


@app.get("/metrics")
def metrics():
    return {"error_rate_percent": 0.5 if healthy else 4.5, "latency_ms": 220 if healthy else 750}

