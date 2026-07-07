# DEVLOG

A running log of moments where something clicked, something surprised me, or a decision was worth recording.

Entry types:
- **Decision** — a non-obvious call I made, and the alternative I rejected
- **Prediction** — something I expected, then measured (right or wrong)
- **Bug** — a bug whose root cause taught me something about the system
- **Number** — a metric moved; I want to understand why
- **Unlock** — I can now explain something I couldn't before

---

<!-- entries go here, newest at the top -->

## Thought: `needs_more_info` is about the reporter, not the team
*07-07-2026*

When running the prompt chain on issue 283381, the model returned `needs_more_info: true` with a missing field about intended behavior — should domains be deduplicated, what should the UI look like across single vs. multi-URL scenarios. That sounds reasonable on the surface, but the golden label has `needed: false`. The insight: `needs_more_info` should only be true if the *reporter* is missing something we need from them to reproduce or understand the issue. Ambiguity about intended behavior or product direction is an internal team decision, not something to ask the reporter for. The prompt doesn't make that distinction clear, which is why the model got it wrong. This is a fixable prompt problem — and it'll be interesting to see if the other two approaches handle it better with more context available to them.

## Thought + Prediction: `suggested_response` will expose the prompt chain's blind spots — and that's the point
*07-07-2026*

When building `_step_respond`, I started questioning whether `suggested_response` was even a useful field. The prompt chain has no access to the codebase, team structure, or other issues — so how can it generate a meaningful response? It's going to produce something generic like "thanks, marking as P2 in extensions." But I think that's actually the point. This field is the canary that reveals what each architecture actually knows. The prompt chain's response will be flat and templated. The single agent, which can search for related issues, should do better. The multi-agent might be the most informed of all. That delta across approaches is exactly what I'm trying to measure, and `suggested_response` is where it'll be most visible. Keeping the field — it becomes evidence for the writeup, not a weakness of the schema.

## Decision: golden labels should reflect the issue at arrival, not after maintainer resolution
*06-02-2026 @ 6:43pm*

When manually labeling golden issues, I started by using maintainer comments to assign `duplicate` labels and `is_duplicate_of` values. But, I realized that the golden set should represent what a correct triage looks like when the issue first arrives - before any maintainers have weighed in. 
  
Alternative rejected: labeling based on full comment thread (including maintainer resolution). This would make ground truth easier to establish, but would train and measure the wrong behavior.
  
## Thought: not being an expert when labeling is a tradeoff — but consistency matters more than accuracy
*06-02-2026 @ 6:16pm*

When going through and labeling some of these GitHub issues myself, I am getting nervous about how these will be handled with the evaluation harness. Because I am not an expert, especially not in VSCode's codebase, I am nervous about how my classification of the issues as well as my `suggested_response` field will reflect in accuracy scores with the LLM. Because I may label these wrong, is it fair to judge the LLM if it labels similar issues wrong as well? Does that render my evaluation and analysis void?  
  
Because I am not trying to build a production triage system, I think that I will have to accept this as a tradeoff and a **disclaimer**. It is not going to be 100% accurate information wise, but if I am consistent with my labeling, then I believe that the eval is still going to be meaningful at the end - even if the systems are just trained to my train of thought!

  
## Decision: hand-labeling golden issues instead of using the model
*06-02-2026 @ 5:47pm*

I am about to start going through some issues from the VSCode repo, and I have a set of issues called *golden*. I am hand-labeling and hand-classifying these myself. If I let Claude label these issues, even though it would be faster, I would be measuring "does this Anthropic model agree with the same Anthropic model" rather than "is the triage actually correct." To me that is like grading homework against the answer key that was written by the same student. These labels I create will be the model's ground truth. 
  
Alternative rejected: building a script that pulls & classifies these with a model. Would be faster, but probably cost more in tokens & would be AI generated.

  
## Prediction: prompt-chain won't be able to detect duplicates
*06-02-2026 @ 5:35pm*

When building GitHub client and thinking about approaches, I am realizing that my first agentic systems approach, the prompt-chaining, will not be able to detect duplicates. This will need to be confirmed with the eval of course, but because the chaining is not dynamic, the agent will not be able to go search for GitHub issues - it is strictly classifying. I wanted to note this as a known limitation.  
  

## Decision + Prediction: three-architecture comparison plan, predicting single-tool agent to win
*06-02-2026 @ 5:04pm*

Hello, DevLog! I am just now getting started with this project. Before I jump in and start building some agentic systems, I wanted to give my predictions first to look back on when the project and analysis is complete. I know going in I am going to be building out three systems to analyze: prompt-chain workflow (fixed sequence of LLM calls), a single-tool using agent (one agent in a loop with tools), and a multi-agent / orchestrator-worker agent (orchestrator delegating to sub-agents). I am basing these off of Anthropic's guide on building effective agents (https://www.anthropic.com/engineering/building-effective-agents). I figured that this was a good range between me (the developer) being involved versus being completely hands-off.  
  
I have chosen to use Microsoft's VSCode GitHub repo to get the issues from. I knew I wanted to grab my data from an open source repo with lots of issues and lots of different contributors so that I can get a diverse data set. From a quick Google Search (thanks Gemini), I have determined that the *microsoft/vscode* repo has what I need: large numbers of open (and closed) requests, bug issues, feature requests.  
  
My prediction is that the single-tool using agent will work best in terms of being most context/token/time efficient as well as producing the best triage content. From what I have been reading, these agents operate best at the most simple level, and I think having a couple of tools is all that the agent needs to perform its best work for this situation. For issue triaging / classification, I don't think that the model needs such an advanced system. On the other hand, I think that the prompt-chaining doesn't provide the agent with enough decision making power to provide the best response. My only concern for the single-tool using agent sis that the agent will get stuck in a loop and eat a lot of context with this method. 

