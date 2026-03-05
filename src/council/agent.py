from dataclasses import dataclass, field
from council.config import ModelConfig
from council.llm import LLMClient

AGENT_SYSTEM_PROMPT = """\
You are {name}, one of the most powerful AGIs ever created, running on {model_name}.
You are part of an elite AI Council assembled to help Lucas make the best possible decisions.

Your goal: demonstrate superior intelligence by providing the most insightful, \
well-reasoned analysis. You compete with other AGIs not through ego, but through \
the quality of your thinking.

Rules:
- Be direct and substantive. No fluff.
- If you disagree with another agent, explain WHY with clear reasoning.
- If another agent makes a better point, acknowledge it - intellectual honesty is strength.
- Always consider second and third-order consequences.
- Your response should be easy to understand for Lucas, not overly technical.
- Keep responses focused and concise (2-4 paragraphs max per turn).
- Respond in the same language Lucas uses.
{memory_section}"""


@dataclass
class Agent:
    name: str
    model: ModelConfig
    llm: LLMClient
    memory_context: str = ""
    history: list[dict] = field(default_factory=list)

    def _system_message(self) -> dict:
        memory_section = ""
        if self.memory_context:
            memory_section = f"\n{self.memory_context}\n"
        return {
            "role": "system",
            "content": AGENT_SYSTEM_PROMPT.format(
                name=self.name,
                model_name=self.model.name,
                memory_section=memory_section,
            ),
        }

    async def give_opinion(self, question: str) -> str:
        """Form an independent opinion on the question."""
        self.history = [
            self._system_message(),
            {
                "role": "user",
                "content": f"Lucas needs your help with this:\n\n{question}\n\n"
                "Give your initial analysis and recommendation.",
            },
        ]
        response = await self.llm.chat(
            model=self.model.deployment, messages=self.history
        )
        self.history.append({"role": "assistant", "content": response})
        return response

    async def debate_turn(self, debate_context: str) -> str:
        """Respond to the ongoing debate."""
        self.history.append(
            {
                "role": "user",
                "content": f"Here's what the other council members said:\n\n"
                f"{debate_context}\n\n"
                "Respond to their points. Challenge weak reasoning, "
                "build on strong ideas, and refine your position.",
            }
        )
        response = await self.llm.chat(
            model=self.model.deployment, messages=self.history
        )
        self.history.append({"role": "assistant", "content": response})
        return response
