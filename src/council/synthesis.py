from council.llm import LLMClient

SYNTHESIS_SYSTEM_PROMPT = """\
You are the Council Synthesizer. You've observed a debate between the world's most \
powerful AGIs. Your job is to produce a clear, friendly summary for Lucas.

Your output MUST include:
1. **Recommendation**: The council's best recommendation, clearly stated
2. **Why**: The key reasoning behind it (keep it simple)
3. **Agreement**: What all agents agreed on
4. **Dissent**: Notable disagreements and why they matter - don't hide them
5. **Confidence**: How confident the council is (high/medium/low) and why
6. **Interesting insights**: The most surprising or valuable points from the debate

Write in the same language Lucas used. Be warm and direct - Lucas is smart but \
doesn't want to wade through jargon. Use short paragraphs.\
"""

SYNTHESIS_MODEL = "gpt-5.3-chat"


async def synthesize(
    question: str,
    transcript: str,
    agent_names: list[str],
    llm: LLMClient,
) -> str:
    messages = [
        {"role": "system", "content": SYNTHESIS_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"Lucas asked: {question}\n\n"
                f"Council members: {', '.join(agent_names)}\n\n"
                f"Full debate transcript:\n\n{transcript}\n\n"
                "Produce your synthesis now."
            ),
        },
    ]
    return await llm.chat(model=SYNTHESIS_MODEL, messages=messages, max_tokens=4000)
