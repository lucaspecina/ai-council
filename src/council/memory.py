import os
from pathlib import Path

# Default: Claude Code's project memory for this repo
DEFAULT_MEMORY_DIR = Path.home() / ".claude" / "projects" / "C--Users-YT40432-Desktop-lp-research-lucaspecina-ai-council" / "memory"


def load_memory(memory_dir: Path | None = None) -> str:
    """Read all .md files from the memory directory and return as context string."""
    directory = memory_dir or Path(os.environ.get("COUNCIL_MEMORY_DIR", str(DEFAULT_MEMORY_DIR)))

    if not directory.exists():
        return ""

    parts = []
    for f in sorted(directory.glob("*.md")):
        content = f.read_text(encoding="utf-8").strip()
        if content:
            parts.append(f"## {f.stem}\n{content}")

    if not parts:
        return ""

    return "# Context about Lucas and this project\n\n" + "\n\n".join(parts)
