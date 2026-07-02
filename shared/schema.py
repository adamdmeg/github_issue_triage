from enum import Enum
from pydantic import BaseModel


class Label(str, Enum):
    bug = "bug"
    feature = "feature"
    docs = "docs"
    question = "question"
    security = "security"
    duplicate = "duplicate"


class Priority(str, Enum):
    P0 = "P0"   # Critical / on fire
    P1 = "P1"   # High
    P2 = "P2"   # Medium
    P3 = "P3"   # Low / nice-to-have


class GitHubIssue(BaseModel):
    number: int
    title: str
    body: str
    comments: list[str] = []


class NeedsMoreInfo(BaseModel):
    needed: bool
    missing: str | None = None


class TriageDecision(BaseModel):
    labels: list[Label]
    priority: Priority
    area: str               # validated at runtime against shared/prompts.AREAS
    needs_more_info: NeedsMoreInfo
    suggested_response: str
    is_duplicate_of: int | None = None  # issue number of the duplicate, if any
