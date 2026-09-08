from functools import lru_cache
from pydantic import BaseModel, Field
import os


class Settings(BaseModel):
    github_token: str = ""
    github_repository: str = ""
    github_branch: str = "main"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    telemetry_url: str = "http://localhost:8000/metrics"
    metrics_timeout_seconds: float = Field(default=5.0, gt=0)
    rollback_enabled: bool = True

    @classmethod
    def from_environment(cls) -> "Settings":
        return cls(
            github_token=os.getenv("GITHUB_TOKEN", ""),
            github_repository=os.getenv("GITHUB_REPOSITORY", ""),
            github_branch=os.getenv("GITHUB_BRANCH", "main"),
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            telemetry_url=os.getenv("TELEMETRY_URL", "http://localhost:8000/metrics"),
            metrics_timeout_seconds=float(os.getenv("METRICS_TIMEOUT_SECONDS", "5")),
            rollback_enabled=os.getenv("ROLLBACK_ENABLED", "true").lower() == "true",
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings.from_environment()

