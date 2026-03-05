import asyncio
import sys
from council.config import Settings
from council.debate import run_debate


def main():
    if len(sys.argv) < 2:
        from rich import print
        print("[bold]Usage:[/bold] python main.py \"your question here\"")
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    settings = Settings()
    settings.validate()

    asyncio.run(run_debate(question, settings))


if __name__ == "__main__":
    main()
