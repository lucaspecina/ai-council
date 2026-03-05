import asyncio
from council.agent import Agent
from council.config import Settings, MODELS
from council.llm import LLMClient
from council.memory import load_memory
from council.synthesis import synthesize
from council import ui


async def run_debate(question: str, settings: Settings):
    """Run a full council debate on the given question."""
    llm = LLMClient(settings)
    memory_context = load_memory()

    agents = [
        Agent(name=model.name, model=model, llm=llm, memory_context=memory_context)
        for model in MODELS
    ]
    agent_colors = {agent.name: ui.get_agent_color(i) for i, agent in enumerate(agents)}

    try:
        ui.print_header(question)

        # Phase 1: parallel initial opinions with live status
        ui.print_phase("Phase 1", "Initial Opinions (parallel)")

        spinners = {}
        for agent in agents:
            spinners[agent.name] = ui.print_agent_thinking(agent.name, agent_colors[agent.name])

        results = await asyncio.gather(
            *[agent.give_opinion(question) for agent in agents],
            return_exceptions=True,
        )

        # Stop all spinners and print results
        for agent in agents:
            spinners[agent.name].stop()

        active_agents = []
        for agent, result in zip(agents, results):
            color = agent_colors[agent.name]
            if isinstance(result, Exception):
                ui.print_agent_offline(agent.name, color, str(result))
            else:
                ui.print_agent_response(agent.name, color, result)
                active_agents.append(agent)

        if not active_agents:
            ui.console.print("[bold red]No agents available. Aborting.[/bold red]")
            return

        ui.print_active_count(len(active_agents), len(agents))

        # Phase 2: sequential debate rounds
        for round_num in range(1, settings.debate_rounds + 1):
            ui.print_phase(f"Round {round_num}", "Debate")

            for agent in active_agents:
                color = agent_colors[agent.name]
                other_statements = []
                for other in active_agents:
                    if other is agent:
                        continue
                    last_msg = _get_last_response(other)
                    if last_msg:
                        other_statements.append(f"[{other.name}]: {last_msg}")

                context = "\n\n".join(other_statements)
                live = ui.print_agent_thinking(agent.name, color)
                try:
                    response = await agent.debate_turn(context)
                    live.stop()
                    ui.print_agent_response(agent.name, color, response)
                except Exception as e:
                    live.stop()
                    ui.print_agent_offline(agent.name, color, str(e))

        # Phase 3: synthesis
        ui.print_phase("Synthesis", "Final recommendation")

        live = ui.print_agent_thinking("Council", "bright_white")

        all_statements = []
        for agent in active_agents:
            for msg in agent.history:
                if msg["role"] == "assistant":
                    all_statements.append(f"[{agent.name}]: {msg['content']}")

        debate_transcript = "\n\n".join(all_statements)
        final = await synthesize(
            question=question,
            transcript=debate_transcript,
            agent_names=[a.name for a in active_agents],
            llm=llm,
        )
        live.stop()
        ui.print_synthesis(final)

    finally:
        await llm.close()


def _get_last_response(agent: Agent) -> str | None:
    for msg in reversed(agent.history):
        if msg["role"] == "assistant":
            return msg["content"]
    return None
