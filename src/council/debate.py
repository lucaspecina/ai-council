import asyncio
from council.agent import Agent
from council.config import ModelConfig, Settings, MODELS
from council.llm import LLMClient
from council.memory import load_memory
from council.synthesis import synthesize


async def run_debate(question: str, settings: Settings) -> str:
    """Run a full council debate on the given question."""
    llm = LLMClient(settings)
    memory_context = load_memory()

    # Create agents - one per model, all share the same memory
    agents = [
        Agent(name=model.name, model=model, llm=llm, memory_context=memory_context)
        for model in MODELS
    ]

    try:
        output_parts = []
        output_parts.append(f"{'='*60}")
        output_parts.append(f"AI COUNCIL - Debate")
        output_parts.append(f"Question: {question}")
        output_parts.append(f"{'='*60}\n")

        # Phase 1: parallel initial opinions
        output_parts.append(f"--- Phase 1: Initial Opinions ---\n")
        opinions = await asyncio.gather(
            *[agent.give_opinion(question) for agent in agents]
        )

        for agent, opinion in zip(agents, opinions):
            output_parts.append(f"[{agent.name}]")
            output_parts.append(f"{opinion}\n")

        # Phase 2: sequential debate rounds
        for round_num in range(1, settings.debate_rounds + 1):
            output_parts.append(f"--- Round {round_num} ---\n")

            for agent in agents:
                # Build context: what others said in this round so far + previous opinions
                other_statements = []
                for other in agents:
                    if other is agent:
                        continue
                    # Get the last assistant message from each other agent
                    last_msg = _get_last_response(other)
                    if last_msg:
                        other_statements.append(f"[{other.name}]: {last_msg}")

                context = "\n\n".join(other_statements)
                response = await agent.debate_turn(context)
                output_parts.append(f"[{agent.name}]")
                output_parts.append(f"{response}\n")

        # Phase 3: synthesis
        output_parts.append(f"--- Synthesis ---\n")

        # Collect all debate content for synthesis
        all_statements = []
        for agent in agents:
            for msg in agent.history:
                if msg["role"] == "assistant":
                    all_statements.append(f"[{agent.name}]: {msg['content']}")

        debate_transcript = "\n\n".join(all_statements)
        final = await synthesize(
            question=question,
            transcript=debate_transcript,
            agent_names=[a.name for a in agents],
            llm=llm,
        )
        output_parts.append(final)
        output_parts.append(f"\n{'='*60}")

        return "\n".join(output_parts)

    finally:
        await llm.close()


def _get_last_response(agent: Agent) -> str | None:
    for msg in reversed(agent.history):
        if msg["role"] == "assistant":
            return msg["content"]
    return None
