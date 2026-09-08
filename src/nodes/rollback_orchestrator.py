from github import Github
from src.config import get_settings
from src.state import ReleaseState


def orchestrate_rollback(state: ReleaseState) -> dict:
    settings = get_settings()
    if state.is_healthy or not settings.rollback_enabled:
        return {"rollback_triggered": False}
    if not settings.github_token or not settings.github_repository:
        raise RuntimeError("Rollback requires GITHUB_TOKEN and GITHUB_REPOSITORY when enabled.")
    repo = Github(settings.github_token).get_repo(settings.github_repository)
    commit = repo.get_commit(state.commit_hash)
    repo.create_git_revert(commit, branch=settings.github_branch)
    return {"rollback_triggered": True}

