---
description: Cómo este proyecto consume LLMs via Azure AI Foundry v1 API. Usar cuando hay que modificar o agregar llamadas a modelos, cambiar endpoints, o debuggear conexiones con Foundry.
---

# Azure AI Foundry v1 API - Patrón del proyecto

## Approach

Usamos la **v1 API** de Foundry (recomendada por Microsoft desde agosto 2025).
- No necesita `api_version`
- Usa `AsyncOpenAI` (no `AsyncAzureOpenAI`) con `base_url`
- Endpoint: `https://<resource>.openai.azure.com/openai/v1/`

## Client (src/council/llm.py)

```python
from openai import AsyncOpenAI

client = AsyncOpenAI(
    base_url=f"{endpoint}/openai/v1/",
    api_key=api_key,
)
```

## Variables de entorno

```bash
AZURE_FOUNDRY_ENDPOINT="https://<resource>.openai.azure.com"  # sin /openai/v1/
AZURE_FOUNDRY_API_KEY="<api-key>"
```

El sufijo `/openai/v1/` se agrega automáticamente en `LLMClient.__init__`.

## Modelos deployados

| Deployment name | Display name |
|----------------|-------------|
| gpt-5.3-chat | GPT-5.3 |
| grok-4-1-fast-reasoning | Grok-4.1 |
| claude-opus-4-6 | Claude Opus 4.6 |
| Kimi-K2.5 | Kimi K2.5 |
| DeepSeek-V3.2 | DeepSeek V3.2 |

## Notas importantes

- `model` param = nombre del **deployment** en Foundry, no el nombre del modelo
- Usar `max_completion_tokens` (no `max_tokens`) para modelos nuevos
- No setear `temperature` explícitamente (GPT-5+ solo soporta 1.0)
- Rate limiting via `asyncio.Semaphore` + retry con backoff exponencial
