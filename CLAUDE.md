# AI Council - Claude Code Instructions

## Project Overview
Multi-agent AI council system where multiple frontier LLMs debate to help Lucas make decisions.
All LLM calls go through Azure AI Foundry using the `openai` SDK (`AsyncAzureOpenAI`).

## Tech Stack
- Python 3.12+ with asyncio
- `openai` SDK (AsyncAzureOpenAI for Foundry)
- No frameworks - pure Python, minimal dependencies

## Architecture
- `src/council/` - main package
  - `config.py` - env vars, model registry, settings
  - `llm.py` - unified async LLM client with retry + rate limiting
  - `agent.py` - Agent class (role, model, personality)
  - `debate.py` - debate orchestrator (parallel opinions -> sequential rounds -> synthesis)
  - `synthesis.py` - synthesize debate into final output
- `main.py` - CLI entry point

## Models (Azure Foundry deployments)
- gpt-5.3-chat
- grok-4-1-fast-reasoning
- claude-opus-4-6
- Kimi-K2.5
- DeepSeek-V3.2

## Conventions
- All LLM calls are async with retry + semaphore + timeout
- Agents are peers (no hierarchy) - they debate as super-intelligent AGIs
- Output must be friendly and easy to understand for Lucas
- Modularity is key - roles and structure will mutate over time
- Parallel execution when possible (e.g., initial opinions), sequential when needed (debate rounds)
- Spanish comments/docs are OK, code in English

## Commands
- Activate env: `conda activate ai-council`
- Run: `python main.py "your question here"`
- Install: `pip install -e .` (already done in conda env)

## Environment
- Conda env: `ai-council` (Python 3.12, miniconda3)
- Config via `.env` file (see `.env.example`)
- Azure Foundry endpoint + API key required
