from src.state import ReleaseState


def aggregate_context(state: ReleaseState) -> dict:
    """Return deterministic local stand-ins for GitHub and Jira context."""
    commit = state.commit_hash or "unknown-commit"
    return {
        "pr_diff": state.pr_diff or f"Commit {commit}: application and deployment changes were submitted for review.",
        "ticket_context": state.ticket_context or f"Jira context for {commit}: standard production release; monitoring and rollback required.",
    }

