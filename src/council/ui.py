from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from rich.live import Live
from rich.spinner import Spinner
from rich.table import Table

console = Console()

# Color per agent (consistent across the debate)
AGENT_COLORS = [
    "cyan",
    "magenta",
    "green",
    "yellow",
    "blue",
]


def get_agent_color(index: int) -> str:
    return AGENT_COLORS[index % len(AGENT_COLORS)]


def print_header(question: str):
    console.print()
    console.print(
        Panel(
            Text(question, style="bold white", justify="center"),
            title="[bold]AI COUNCIL[/bold]",
            subtitle="5 AGIs debating for you",
            border_style="bright_white",
            padding=(1, 4),
        )
    )
    console.print()


def print_phase(title: str, description: str = ""):
    text = f"[bold]{title}[/bold]"
    if description:
        text += f"  [dim]{description}[/dim]"
    console.print(Rule(text, style="bright_white"))
    console.print()


def print_agent_thinking(name: str, color: str) -> Live:
    spinner = Spinner("dots", text=Text(f" {name} is thinking...", style=f"dim {color}"))
    live = Live(spinner, console=console, transient=True)
    live.start()
    return live


def print_agent_response(name: str, color: str, response: str):
    console.print(
        Panel(
            Markdown(response),
            title=f"[bold {color}]{name}[/bold {color}]",
            border_style=color,
            padding=(0, 2),
        )
    )
    console.print()


def print_agent_offline(name: str, color: str, error: str):
    console.print(
        Panel(
            Text(f"OFFLINE: {error}", style="dim red"),
            title=f"[bold {color}]{name}[/bold {color}]",
            border_style="red",
            padding=(0, 2),
        )
    )
    console.print()


def print_active_count(active: int, total: int):
    style = "green" if active == total else "yellow"
    console.print(f"  [{style}]{active}/{total} agents active[/{style}]\n")


def print_synthesis(response: str):
    console.print(
        Panel(
            Markdown(response),
            title="[bold white]COUNCIL SYNTHESIS[/bold white]",
            border_style="bright_white",
            padding=(1, 3),
        )
    )
    console.print()
