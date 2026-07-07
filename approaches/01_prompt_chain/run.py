import json
import sys
from pathlib import Path

from shared.github_client import fetch_issue
from shared.prompts import REPO
from shared.schema import GitHubIssue
from .chain import run_chain


def load_issue(number: int) -> GitHubIssue:
    local = Path(f"data/issues/{number}.json")
    if local.exists():
        return GitHubIssue(**json.loads(local.read_text()))
    print(f"No local file found for #{number}, fetching from GitHub...")
    return fetch_issue(REPO, number)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m approaches.01_prompt_chain.run <issue_number>")
        sys.exit(1)

    number = int(sys.argv[1])
    issue = load_issue(number)
    decision = run_chain(issue)
    print(decision.model_dump_json(indent=2))
