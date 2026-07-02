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

## Decision + Prediction: 06-02-2026 @ 5:04pm
Hello, DevLog! I am just now getting started with this project. Before I jump in and start building some agentic systems, I wanted to give my predictions first to look back on when the project and analysis is complete. I know going in I am going to be building out three systems to analyze: prompt-chain workflow (fixed sequence of LLM calls), a single-tool using agent (one agent in a loop with tools), and a multi-agent / orchestrator-worker agent (orchestrator delegating to sub-agents). I am basing these off of Anthropic's guide on building effective agents (https://www.anthropic.com/engineering/building-effective-agents). I figured that this was a good range between me (the developer) being involved versus being completely hands-off.  
  
I have chosen to use Microsoft's VSCode GitHub repo to get the issues from. I knew I wanted to grab my data from an open source repo with lots of issues and lots of different contributors so that I can get a diverse data set. From a quick Google Search (thanks Gemini), I have determined that the *microsoft/vscode* repo has what I need: large numbers of open (and closed) requests, bug issues, feature requests.  
  
My prediction is that the single-tool using agent will work best in terms of being most context/token/time efficient as well as producing the best triage content. From what I have been reading, these agents operate best at the most simple level, and I think having a couple of tools is all that the agent needs to perform its best work for this situation. For issue triaging / classification, I don't think that the model needs such an advanced system. On the other hand, I think that the prompt-chaining doesn't provide the agent with enough decision making power to provide the best response. My only concern for the single-tool using agent sis that the agent will get stuck in a loop and eat a lot of context with this method. 

