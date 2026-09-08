import argparse
from src.graph import release_graph
from src.state import ReleaseState


def main() -> None:
    parser = argparse.ArgumentParser(description="Agentic release readiness orchestrator")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--commit", required=True)
    args = parser.parse_args()
    result = release_graph.invoke(ReleaseState(repo_name=args.repo, commit_hash=args.commit))
    print(ReleaseState.model_validate(result).model_dump_json(indent=2))


if __name__ == "__main__":
    main()

