import os
import requests
from shared.schema import GitHubIssue

_BASE = "https://api.github.com"


def _headers() -> dict:
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def fetch_issue(repo: str, number: int) -> GitHubIssue:
    """Fetch a single issue and its comments from GitHub."""
    issue_resp = requests.get(f"{_BASE}/repos/{repo}/issues/{number}", headers=_headers())
    issue_resp.raise_for_status()
    issue_data = issue_resp.json()

    comments_resp = requests.get(issue_data["comments_url"], headers=_headers())
    comments_resp.raise_for_status()
    comments = [c["body"] for c in comments_resp.json()]

    return GitHubIssue(
        number=issue_data["number"],
        title=issue_data["title"],
        body=issue_data["body"] or "",
        comments=comments,
    )


def search_issues(repo: str, query: str, max_results: int = 10) -> list[GitHubIssue]:
    """Search issues in a repo using GitHub's search API."""
    params = {"q": f"{query} repo:{repo} is:issue", "per_page": max_results}
    resp = requests.get(f"{_BASE}/search/issues", headers=_headers(), params=params)
    resp.raise_for_status()

    results = []
    for item in resp.json().get("items", []):
        results.append(GitHubIssue(
            number=item["number"],
            title=item["title"],
            body=item["body"] or "",
        ))
    return results
