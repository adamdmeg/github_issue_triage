# github_issue_triage

A learning experiment comparing three agentic AI architectures on the same task: triaging GitHub issues into a structured decision. The goal isn't just to build something that works — it's to understand how architecture shape affects output quality, token usage, and observability when building with LLMs.

I'm using issues from [microsoft/vscode](https://github.com/microsoft/vscode) as the dataset. High volume, diverse issue types, lots of contributors — good range of signal.

---

## what it does

Given a GitHub issue (title, body, optional comments), each approach produces a `TriageDecision`:

| field | description |
|---|---|
| `labels` | bug, feature, docs, question, security, or duplicate |
| `priority` | P0 (critical) → P3 (low) |
| `area` | which component or subsystem the issue belongs to |
| `needs_more_info` | whether the issue needs clarification, and what's missing |
| `suggested_response` | a draft first reply to the issue author |
| `is_duplicate_of` | issue number if a duplicate, otherwise null |

All three approaches produce the same output schema — what differs is how they get there.

---

## three approaches

**01 — prompt chain**
Sequential prompts where each step builds on the last (classify → prioritize → respond). Predictable and easy to debug, but no ability to look things up dynamically — which means it likely can't detect duplicates.

**02 — single tool-using agent**
One agent with tools (`fetch_issue`, `search_issues`) that decides what information it needs before triaging. More flexible, and should be able to handle duplicate detection.

**03 — multi-agent orchestrator + workers**
An orchestrator dispatches to specialist workers (labeling, duplicate detection, response drafting). Highest complexity — I want to see if the added coordination overhead is worth it.

My prediction going in: the single-agent approach will perform best for this task. I think the added complexity of multi-agent coordination isn't necessary for issue triage, and the prompt chain won't have enough decision-making power.

---

## eval

Each approach is evaluated against a hand-labeled golden set of vscode issues. I labeled these myself rather than using a model — if I'd used Claude to label the ground truth and then measured Claude's output against it, I'd just be measuring "does this model agree with itself."

Fields are scored by exact match: labels, priority, area, needs_more_info, is_duplicate_of. `suggested_response` is evaluated qualitatively.

---

## stack

- Python 3.11+
- Anthropic SDK
- Pydantic v2
- requests

---

## setup

```bash
pip install -e ".[dev]"
cp .env.example .env  # add ANTHROPIC_API_KEY and GITHUB_TOKEN
```

## run an approach

```bash
python -m approaches.01_prompt_chain.run <issue_number>
python -m approaches.02_single_agent.run <issue_number>
python -m approaches.03_multi_agent.run <issue_number>
```

## run the eval

```bash
python -m shared.eval.harness
```

---

## project layout

```
shared/          # schema, github client, prompt constants, eval harness
approaches/
  01_prompt_chain/   # sequential prompts
  02_single_agent/   # one agent with tools
  03_multi_agent/    # orchestrator + specialist workers
data/
  issues/        # raw github issues as JSON
  golden/        # hand-labeled TriageDecision ground truth
results/         # eval outputs
```

Each `approaches/` directory has its own README with design rationale and observed tradeoffs. `DEVLOG.md` tracks decisions, predictions, and things that surprised me along the way.
