# AI Council

A council of the world's most powerful AGIs debating with each other to help you make the best possible decisions.

5 frontier models receive your question, form independent opinions in parallel, then debate each other in sequential rounds. A final synthesis distills the debate into a clear recommendation — highlighting agreements, dissents, and the most interesting insights.

## Models

| Agent | Model |
|-------|-------|
| GPT-5.3 | `gpt-5.3-chat` |
| Grok-4.1 | `grok-4-1-fast-reasoning` |
| Claude Opus 4.6 | `claude-opus-4-6` |
| Kimi K2.5 | `Kimi-K2.5` |
| DeepSeek V3.2 | `DeepSeek-V3.2` |

All models are consumed via Azure AI Foundry v1 API.

## Setup

```bash
# Create conda environment
conda create -n ai-council python=3.12 -y
conda activate ai-council

# Install
pip install -e .

# Configure credentials
cp .env.example .env
# Edit .env with your Azure AI Foundry endpoint and API key
```

### .env

```bash
AZURE_FOUNDRY_ENDPOINT="https://<resource>.openai.azure.com"
AZURE_FOUNDRY_API_KEY="<your-api-key>"
MAX_CONCURRENT_CALLS=10
DEBATE_ROUNDS=2
```

The endpoint and API key are in the Azure portal: Azure AI Foundry > your resource > Keys and Endpoint.

## Usage

```bash
conda activate ai-council
python main.py "Should I learn Rust or Go as a second language?"
```

## How it works

```
Question
   |
   v
Phase 1: Initial Opinions (parallel)
   All 5 models answer independently at the same time
   |
   v
Phase 2: Debate (sequential rounds)
   Each model sees what the others said and responds
   They challenge, build on ideas, or change positions
   Default: 2 rounds
   |
   v
Phase 3: Synthesis
   Produces: recommendation, agreements, dissents,
   confidence level, and interesting insights
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `AZURE_FOUNDRY_ENDPOINT` | — | Azure AI Foundry endpoint |
| `AZURE_FOUNDRY_API_KEY` | — | API key |
| `MAX_CONCURRENT_CALLS` | 10 | Max parallel LLM calls |
| `DEBATE_ROUNDS` | 2 | Number of debate rounds |
| `COUNCIL_MEMORY_DIR` | auto | Override memory directory path |
