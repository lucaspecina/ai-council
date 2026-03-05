import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class ModelConfig:
    deployment: str
    name: str


# Modelos disponibles en Foundry
MODELS = [
    ModelConfig(deployment="gpt-5.3-chat", name="GPT-5.3"),
    ModelConfig(deployment="grok-4-1-fast-reasoning", name="Grok-4.1"),
    ModelConfig(deployment="claude-opus-4-6", name="Claude Opus 4.6"),
    ModelConfig(deployment="Kimi-K2.5", name="Kimi K2.5"),
    ModelConfig(deployment="DeepSeek-V3.2", name="DeepSeek V3.2"),
]


@dataclass
class Settings:
    azure_endpoint: str = field(
        default_factory=lambda: os.environ.get("AZURE_FOUNDRY_ENDPOINT", "")
    )
    azure_api_key: str = field(
        default_factory=lambda: os.environ.get("AZURE_FOUNDRY_API_KEY", "")
    )
    max_concurrent: int = field(
        default_factory=lambda: int(os.environ.get("MAX_CONCURRENT_CALLS", "10"))
    )
    debate_rounds: int = field(
        default_factory=lambda: int(os.environ.get("DEBATE_ROUNDS", "2"))
    )

    def validate(self):
        if not self.azure_endpoint:
            raise ValueError("AZURE_FOUNDRY_ENDPOINT is required")
        if not self.azure_api_key:
            raise ValueError("AZURE_FOUNDRY_API_KEY is required")
