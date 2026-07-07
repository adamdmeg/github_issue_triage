import json
import re
import anthropic
from shared.schema import GitHubIssue, TriageDecision, Label, Priority, NeedsMoreInfo
from shared.prompts import AREAS

_client = anthropic.Anthropic()


def _issue_text(issue: GitHubIssue) -> str:
    parts = [f"Title: {issue.title}", f"Body:\n{issue.body}"]
    if issue.comments:
        comments_block = "\n-----\n".join(issue.comments)
        parts.append(f"Comments:\n-----\n{comments_block}\n-----")
    return "\n\n".join(parts)


def _step_summarize(raw: str) -> str:
    response = _client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=512,
        system=(
            "You are a technical issue summarizer for a software project. "
            "Your job is to distill a GitHub issue into one plain-text paragraph "
            "that captures what the reporter is experiencing or requesting. "
            "Ignore HTML tags, template boilerplate, step-by-step reproduction "
            "checklists, and system info tables — focus only on the core problem or request."
        ),
        messages=[
            {
                "role": "user",
                "content": (
                    "Summarize the following GitHub issue in one paragraph. "
                    "Write in plain text, no markdown or bullet points.\n\n"
                    f"{raw}"
                ),
            }
        ],
    )
    return next(b.text for b in response.content if b.type == "text")


def _step_classify(raw: str, summary: str) -> dict:
    areas_list = ", ".join(AREAS)
    response = _client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=512,
        system=(
            "You are a GitHub issue classifier for a software project. "
            "You will be given a summary of an issue and its raw text. "
            "Return a JSON object inside a ```json code block with exactly these fields:\n"
            '  "labels": list of one or more from ["bug", "feature", "docs", "question", "security", "duplicate"]\n'
            '  "priority": one of "P0", "P1", "P2", "P3"\n'
            f'  "area": one of [{areas_list}]\n'
            '  "needs_more_info": {"needed": true/false, "missing": null or a short string describing what is missing}\n'
            "Priority guide: P0=service down/data loss, P1=major feature broken, P2=significant bug/backlog, P3=minor/cosmetic."
        ),
        messages=[
            {
                "role": "user",
                "content": (
                    f"Summary:\n{summary}\n\n"
                    f"Raw issue:\n{raw}"
                ),
            }
        ],
    )
    text = next(b.text for b in response.content if b.type == "text")
    match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    return json.loads(match.group(1) if match else text)


def _step_respond(raw: str, summary: str, classification: dict) -> str:
    response = _client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=256,
        system=(
            "You are a GitHub maintainer writing a brief response to a new issue. "
            "You have already classified the issue. Write one short sentence addressed to the reporter — "
            "acknowledge what they reported and state the action being taken. "
            "Maximum 20 words. No markdown, no bullet points, plain text only."
        ),
        messages=[
            {
                "role": "user",
                "content": (
                    f"Issue summary: {summary}\n\n"
                    f"Classification: {json.dumps(classification)}\n\n"
                    f"Raw issue:\n{raw}"
                ),
            }
        ],
    )
    return next(b.text for b in response.content if b.type == "text")


def run_chain(issue: GitHubIssue) -> TriageDecision:
    raw = _issue_text(issue)
    summary = _step_summarize(raw)
    classification = _step_classify(raw, summary)
    suggested_response = _step_respond(raw, summary, classification)
    return TriageDecision(
        labels=[Label(l) for l in classification["labels"]],
        priority=Priority(classification["priority"]),
        area=classification["area"],
        needs_more_info=NeedsMoreInfo(**classification["needs_more_info"]),
        suggested_response=suggested_response,
        is_duplicate_of=None,
    )
