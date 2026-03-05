# AI Council

## Vision
A council of the world's most powerful AGIs debating with each other to help Lucas make the best possible decisions. They're not pretending to be human experts - they ARE superintelligent AIs competing to demonstrate who provides the most brilliant insights.

## How it Works

### Phase 1: Initial Opinions (parallel)
All agents receive the question simultaneously and form their independent opinion. This runs in parallel since opinions are independent.

### Phase 2: Debate (sequential rounds)
Agents see all initial opinions and take turns responding, challenging, and refining. Each round, every agent sees the full conversation history and can:
- Challenge other agents' reasoning
- Build on good ideas from others
- Change their position if convinced (showing intellectual honesty)
- Point out blind spots

### Phase 3: Synthesis
A designated synthesizer (rotating role) produces:
- The council's recommendation
- Key points of agreement
- Notable dissents and why they matter
- Confidence level
- A friendly, clear explanation for Lucas

### Phase 4: Follow-up (interactive loop)
After synthesis, the terminal stays alive. Lucas can:
- Ask follow-up questions that trigger new debate rounds with full prior context
- Type "exit" or Ctrl+C to end the session
- Resume later with `--continue` (last session) or `--resume <id>`

### Session Persistence
Each debate is a **session** stored in `~/.ai-council/sessions/{session_id}/`:
- `metadata.json` — question, timestamp, agents, status (active/completed)
- `transcript.json` — full agent histories, phases, synthesis results

This allows:
- Resuming debates across terminal sessions
- Building long-running decision threads with multiple follow-ups
- Future: feeding past decisions as context for new debates

## Design Principles
- **Modular**: agents, roles, debate format - everything can change
- **Parallel when possible**: independent operations run concurrently
- **Model diversity**: each agent runs on a different frontier model
- **No hierarchy**: all agents are peers in debate
- **Transparency**: show the reasoning, disagreements, and how conclusions were reached

## Models
| Agent | Model (Foundry deployment) |
|-------|---------------------------|
| Agent 1 | gpt-5.3-chat |
| Agent 2 | grok-4-1-fast-reasoning |
| Agent 3 | claude-opus-4-6 |
| Agent 4 | Kimi-K2.5 |
| Agent 5 | DeepSeek-V3.2 |
