# TODO

## v0.1 - Foundation
- [x] Project structure and config
- [x] Unified LLM client (Foundry async with retry)
- [x] Agent class with model binding
- [x] Debate orchestrator (opinions -> rounds -> synthesis)
- [x] Synthesis module
- [x] CLI entry point
- [x] Test with real Foundry deployments (4/5 working, Claude Opus in different resource)
- [x] Rich terminal UI (panels, colors, spinners, markdown rendering)
- [ ] Fix Claude Opus 4.6 deployment (different Foundry resource)

## v0.2 - Sessions & Continuations (PRIORITY)
Session persistence and interactive follow-ups. This is the core UX.

### Session Storage (`~/.ai-council/sessions/{session_id}/`)
- [ ] Generate session_id per debate (timestamp + short hash, e.g. `20260305-a3f2`)
- [ ] `metadata.json`: question, timestamp, agents used, status (active/completed)
- [ ] `transcript.json`: full state — each agent's message history, phases, synthesis
- [ ] Store enough state to fully reconstruct agent histories and resume debate

### Interactive Loop
- [ ] After synthesis, terminal stays alive waiting for user input
- [ ] User can type a follow-up question → triggers new debate round with full prior context
- [ ] Follow-up injects into all active agents' histories as continuation
- [ ] New synthesis after each follow-up round
- [ ] Ctrl+C or "exit" gracefully ends the session (status → completed)

### CLI Resume
- [ ] `python main.py "question"` — new session
- [ ] `python main.py --continue` — resume last active session
- [ ] `python main.py --resume <session_id>` — resume specific session
- [ ] `python main.py --list` — list past sessions (id, question, date, status)
- [ ] On resume: reload agent histories from transcript.json, show previous synthesis, wait for input

### Display on Resume
- [ ] Show compact summary of previous debate (question + synthesis only, not full transcript)
- [ ] Then wait for follow-up input
- [ ] Option `--full` to replay entire transcript on resume

## v0.3 - Foundry Agents (upgrade from raw model calls)
- [ ] Migrate from chat completions to Azure AI Foundry Agents API
- [ ] Each council member becomes a Foundry Agent with tools:
  - [ ] Web search (Bing grounding) - agents can look up real-time data
  - [ ] Code interpreter - agents can run code to validate claims
  - [ ] File search - agents can reference uploaded documents
- [ ] Agent threads for conversation state (instead of manual history)
- [ ] Tool usage visible in output (show when an agent searches or runs code)

## v0.4 - Memory & Context
- [ ] Memory system (agents remember past decisions and outcomes)
- [ ] Feed previous decisions as context for new debates
- [ ] User profile: preferences, goals, constraints that agents always know

## v0.5 - Debate Formats
- [ ] Configurable debate formats (structured, freeform, devil's advocate)
- [ ] Agent personas/specializations
- [ ] Custom agent roles (optimizer, critic, devil's advocate)
- [ ] Agent voting system with weighted confidence

## Future
- [ ] Web UI
- [ ] Cost tracking per debate
- [ ] Streaming tokens (show text appearing in real-time, not just spinner → full response)
- [ ] Streaming API for real-time debate consumption
